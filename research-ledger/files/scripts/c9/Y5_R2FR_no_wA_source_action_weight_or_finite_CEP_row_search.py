from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1604"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1604-Y5-R2FR-no-wA-source-action-weight-or-finite-C_EP-row-search.md"

SOURCE_FILES = {
    "1603_doc": ROOT / "1603-Y5-R2FR-source-label-forgetting-or-finite-C_EP-source-pack.md",
    "1603_validation": OUT / "P8_Y5_BRR545_1603_VALIDATION.csv",
    "1603_slf": OUT / "P8_Y5_PARENT_QLOC_1603_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv",
    "1603_validator": OUT / "P8_Y5_PARENT_QLOC_1603_FINITE_CEP_VALIDATOR_SPEC.csv",
    "1603_template": OUT / "P8_Y5_PARENT_QLOC_1603_FINITE_CEP_SOURCE_PACK_TEMPLATE.csv",
    "1449_zero": OUT / "P8_Y5_R10_1449_C_PARENT_ZERO_DERIVATION_ATTEMPT.csv",
    "1593_zero": OUT / "P8_Y5_PARENT_QLOC_1593_CANONICAL_COUPLING_ZERO_THEOREM_ATTEMPT.csv",
    "1593_residual": OUT / "P8_Y5_PARENT_QLOC_1593_ACTION_WEIGHT_SOURCE_RESIDUAL.csv",
    "1594_action_weight": OUT / "P8_Y5_PARENT_QLOC_1594_ACTION_WEIGHT_EXCLUSION_THEOREM_ATTEMPT.csv",
    "1478_single_action": COEFF / "single_action_density_line_proof_attempt_nonclaim_1478.csv",
    "1479_no_source_prefactor": COEFF / "no_source_only_prefactor_typing_theorem_nonclaim_1479.csv",
    "1470_typed_grammar": COEFF / "typed_visible_action_grammar_attempt_1470.csv",
    "1450_hilbert_forgetting": COEFF / "Hilbert_source_label_forgetting_theorem_attempt_1450.csv",
    "1452_common_measure": COEFF / "common_measure_current_theorem_attempt_1452.csv",
    "1453_current_owner": COEFF / "current_source_normalization_owner_theorem_attempt_1453.csv",
    "1476_source_label": COEFF / "source_label_forgetting_proof_attempt_nonclaim_1476.csv",
    "1485_refusal": COEFF / "C_parent_WEP_import_refusal_nonclaim_1485.csv",
    "1442_slot_template": COEFF / "C_parent_WEP_slot_import_TEMPLATE.csv",
}

NEEDLES = {
    "1603_doc": ["NEXT_1604_NO_WA_SOURCE_ACTION_WEIGHT_OR_FINITE_ROW_SEARCH", "no-w_A"],
    "1603_validation": ["VAL1603_OVERALL", "PASS"],
    "1603_slf": ["SLF1603_5_verdict", "C_EP_ZERO_NOT_CERTIFIED"],
    "1603_validator": ["FCV1603_4_zero_policy", "REJECT_CLOSURE_ONLY_ZERO"],
    "1603_template": ["FCT1603_0_C_EP_source_pack_template", "TEMPLATE_ONLY_NOT_IMPORTABLE"],
    "1449_zero": ["DZ1449_4_source_weight_term", "COUNTERMODEL_SURVIVES"],
    "1593_zero": ["ZTH1593_5_no_action_weights", "ACTIVE_COUNTEREXAMPLE"],
    "1593_residual": ["SWR1593_1_relative_weight", "FIRST_FILL_ROW_READY_VALUE_MISSING"],
    "1594_action_weight": ["AWT1594_7_verdict", "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED_VALIDATOR_REQUIRED"],
    "1478_single_action": ["SAL1478_4_verdict", "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED"],
    "1479_no_source_prefactor": ["NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"],
    "1470_typed_grammar": ["TNG1470_5_verdict", "NOT_PARENT_DERIVED_START_SOURCE_FILL"],
    "1450_hilbert_forgetting": ["HT1450_3_relative_prefactor_counterexample", "COUNTEREXAMPLE_SURVIVES"],
    "1452_common_measure": ["CMT1452_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
    "1453_current_owner": ["CSO1453_5_pre_variation_weight", "SURVIVES_PRE_VARIATION"],
    "1476_source_label": ["SLF1476_3_countermodel", "relative source-weight countermodel remains live"],
    "1485_refusal": ["IMP1485_4_bound_inversion", "REFUSED_BOUND_INVERSION_FORBIDDEN"],
    "1442_slot_template": ["CP_WEP_TiPt_TEMPLATE", "TEMPLATE_ONLY_NOT_IMPORTABLE"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1604_SOURCE_REGISTER.csv"
NO_WA = OUT / "P8_Y5_PARENT_QLOC_1604_NO_WA_THEOREM_ATTEMPT.csv"
ACTION_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1604_SOURCE_ACTION_WEIGHT_CONTRACT.csv"
COUNTERMODEL = OUT / "P8_Y5_PARENT_QLOC_1604_WA_COUNTERMODEL_AUDIT.csv"
FINITE_SEARCH = OUT / "P8_Y5_PARENT_QLOC_1604_FINITE_CEP_ROW_SEARCH.csv"
VALIDATOR_DRY_RUN = OUT / "P8_Y5_PARENT_QLOC_1604_FINITE_CEP_VALIDATOR_DRY_RUN.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1604_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1604_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1604_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1604_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1604_VALIDATION.csv"

COPY_TARGETS = {
    NO_WA: [
        QUARANTINE / "NO_WA_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_no_wA_theorem_attempt_nonclaim_1604.csv",
    ],
    ACTION_CONTRACT: [
        QUARANTINE / "SOURCE_ACTION_WEIGHT_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_source_action_weight_contract_nonclaim_1604.csv",
    ],
    COUNTERMODEL: [
        QUARANTINE / "WA_COUNTERMODEL_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_wA_countermodel_audit_nonclaim_1604.csv",
    ],
    FINITE_SEARCH: [
        QUARANTINE / "FINITE_CEP_ROW_SEARCH_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_CEP_row_search_nonclaim_1604.csv",
    ],
    VALIDATOR_DRY_RUN: [
        QUARANTINE / "FINITE_CEP_VALIDATOR_DRY_RUN_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_CEP_validator_dry_run_nonclaim_1604.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1604.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1604_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1604_no_wA_or_finite_CEP_row_search_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def no_wa_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NWA1604_0_target",
            "claim_piece": "no independent pre-variation ordinary-matter source/action weights",
            "formal_statement": "S_ord = int dmu_parent L_ord(Psi_A, gauge, theta_A, e_obs)/hbar_parent with no independent sum_A w_A S_A slots except a common quotient-equivalent constant w_*.",
            "proof_status": "TARGET_RESTATED",
            "blocking_gap": "parent action-density owner still not signed",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NWA1604_1_chain_rule_if_domain_closed",
            "claim_piece": "conditional chain-rule zero",
            "formal_statement": "If every source coefficient factors through q(Phi), total Hilbert current, fixed representation data, and one shared measure, then Dq[v]=0 and on-shell/boundary silence imply delta_v S_ord has no relative source-weight term.",
            "proof_status": "EXACT_CONDITIONAL_LEMMA",
            "blocking_gap": "domain closure and measure ownership are assumptions, not parent-derived statements",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NWA1604_2_common_weight_absorption",
            "claim_piece": "common action scale is not a WEP/source residual",
            "formal_statement": "w_A=w_* for all A can be absorbed into the common action normalization/G calibration only if it is constant, species-blind, field-independent, and carries no range/readout dependence.",
            "proof_status": "CONDITIONAL_CALIBRATION_GUARD",
            "blocking_gap": "relative Delta_w_A and phi-dependent beta_w_A are not absorbed",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NWA1604_3_no_source_only_slot",
            "claim_piece": "source-only prefactor typing",
            "formal_statement": "Hom_parent(species_label or hidden_marker, R_+^active-source-prefactor) must be absent or common-constant only before variation.",
            "proof_status": "EXACT_AS_CONTRACT_NOT_PARENT_SIGNED",
            "blocking_gap": "existing corpus has no primitive object-language axiom forbidding the slot",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NWA1604_4_common_measure_owner",
            "claim_piece": "single action density and measure owner",
            "formal_statement": "One parent measure, one hbar/action scale, one source-normalization current owner, and no species Jacobian J_A would collapse independent w_A into w_*.",
            "proof_status": "CONDITIONAL_NOT_REDUCED",
            "blocking_gap": "species Jacobian/direct-sum component countermodel survives",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NWA1604_5_current_owner_limit",
            "claim_piece": "current ownership cannot erase pre-action weights",
            "formal_statement": "Hilbert/source current ownership kills post-variation rescaling, but if w_A is already inside S_matter before variation, T_H inherits w_A.",
            "proof_status": "SURVIVES_PRE_VARIATION",
            "blocking_gap": "no-w_A must be proven at the parent action level",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NWA1604_6_readout_and_nonHilbert_guard",
            "claim_piece": "no reentry after variation",
            "formal_statement": "No non-Hilbert current, boundary term, source-worldtube selector, detector/readout kernel, or hidden marker may recreate species weights after the Hilbert source is formed.",
            "proof_status": "PARALLEL_GATES_OPEN",
            "blocking_gap": "readout no-reentry and non-Hilbert silence remain unsigned",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NWA1604_7_verdict",
            "claim_piece": "no-w_A theorem status",
            "formal_statement": "No-w_A is a clean conditional theorem, but the parent action has not yet forced one action-density owner and has not excluded all source-only prefactor slots.",
            "proof_status": "NO_WA_NOT_DERIVED",
            "blocking_gap": "S_matter=sum_A w_A S_A remains legal in the current corpus",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def action_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "CON1604_0_action_density_owner",
            "required_parent_signature": "ordinary matter is generated by one parent action-density line, not a direct sum of independently normalizable source sectors",
            "would_prove": "relative w_A slots are not legal parent degrees of freedom",
            "current_status": "UNSIGNED",
            "acceptance_test": "source file must state S_ord owner and forbid independent species action weights before variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "CON1604_1_common_measure",
            "required_parent_signature": "one shared measure/Jacobian and one hbar/action scale for all ordinary matter sectors",
            "would_prove": "species Jacobian J_A and relative action scales collapse to common calibration or vanish",
            "current_status": "UNSIGNED",
            "acceptance_test": "no Dmu_parent=product_A J_A Dpsi_A or equivalent source-only measure factor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "CON1604_2_typed_domain",
            "required_parent_signature": "source coefficients may depend only on observable geometry, dynamical fields, fixed representation data, and universal constants",
            "would_prove": "hidden markers/species labels cannot map into active-source coefficients",
            "current_status": "UNSIGNED",
            "acceptance_test": "Hom_parent(species_label or hidden_marker, source_prefactor) is absent or common-constant only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "CON1604_3_current_owner",
            "required_parent_signature": "Hilbert/coframe current is the only local gravitational source current or all non-Hilbert bypasses are exact/projected-silent",
            "would_prove": "post-variation source normalization and zeta_A bypasses cannot mimic relative w_A",
            "current_status": "PARTIAL_CONDITIONAL_ONLY",
            "acceptance_test": "variation-before-readout and no non-Hilbert current clauses are parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "CON1604_4_readout_no_reentry",
            "required_parent_signature": "detector/source-worldtube/readout maps cannot reintroduce source labels into the parent coupling after variation",
            "would_prove": "finite C_EP cannot be recreated downstream by reporting kernels",
            "current_status": "UNSIGNED",
            "acceptance_test": "readout kernels are explicitly downstream observables, not source-coupling arguments",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "WAC1604_0_direct_sum_weight",
            "countermodel": "S_matter = sum_A w_A S_A with constant species-dependent w_A",
            "survives_because": "covariance, locality, and additivity are preserved inside each sector",
            "damage_if_live": "T_source = sum_A w_A T_A, so active gravitational source is composition-dependent",
            "status": "LIVE_COUNTERMODEL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "WAC1604_1_classical_eom_scaling",
            "countermodel": "delta(w_A S_A)/delta Psi_A=0 may have the same isolated matter equations as delta S_A/delta Psi_A=0",
            "survives_because": "classical EOM equality does not fix Hilbert-source normalization",
            "damage_if_live": "same matter trajectories can still source geometry differently",
            "status": "FALSE_PROOF_ROUTE_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "WAC1604_2_common_G_absorption_guard",
            "countermodel": "hide relative w_A in measured G_N",
            "survives_because": "only a universal constant w_* is calibration; relative, derivative, range, or composition dependence is physical",
            "damage_if_live": "Newton/GR source normalization remains unproved rather than calibrated away",
            "status": "ABSORPTION_SHORTCUT_REJECTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "WAC1604_3_phi_dependent_weight",
            "countermodel": "w_A(phi) gives beta_w_A and finite scalar/source exchange products",
            "survives_because": "no parent theorem forbids field-dependent source weights yet",
            "damage_if_live": "R10/PPN/WEP finite rows require sourced beta/source products",
            "status": "LIVE_PARAMETER_ROUTE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "WAC1604_4_verdict",
            "countermodel": "all no-w_A shortcuts",
            "survives_because": "the only safe closure is a parent action-density/measure/domain theorem or a source-backed finite coefficient row",
            "damage_if_live": "C_EP zero route and local-GR source-universality remain blocked",
            "status": "KEEP_DELTA_W_VECTOR_LIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


REQUIRED_FINITE_FIELDS = [
    "same_parent_branch_id",
    "schema_version",
    "coefficient_id",
    "quantity",
    "value",
    "uncertainty",
    "units",
    "sign_convention",
    "basis",
    "source_path",
    "parent_status",
    "zero_certificate_status",
    "no_bound_inversion",
    "no_tau_unity",
    "valid_for_claim",
    "claim_allowed",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def candidate_paths() -> list[Path]:
    paths: list[Path] = [
        COEFF / "C_parent_WEP_slot_import.csv",
        OUT / "P8_Y5_PARENT_QLOC_1603_FINITE_CEP_SOURCE_PACK_TEMPLATE.csv",
        COEFF / "C_parent_WEP_slot_import_TEMPLATE.csv",
    ]
    patterns = ["*C*EP*.csv", "*C_parent_WEP*slot*.csv"]
    for folder in (OUT, COEFF):
        if folder.exists():
            for pattern in patterns:
                for path in folder.glob(pattern):
                    if "1604" not in path.name and path not in paths:
                        paths.append(path)
    return paths


def is_real_source(source_path: str) -> bool:
    value = source_path.strip()
    lower = value.lower()
    if not value or value.startswith("MISSING_"):
        return False
    if lower.startswith(("http://", "https://", "doi:")):
        return True
    path = Path(value)
    if path.is_absolute():
        return path.exists()
    return (ROOT / value).exists() or (OUT / value).exists() or (COEFF / value).exists()


def is_finite_numeric(value: str) -> bool:
    try:
        numeric = float(value)
    except ValueError:
        return False
    return math.isfinite(numeric)


def validate_candidate_row(row: dict[str, str], path: Path) -> tuple[str, str, bool]:
    missing = [field for field in REQUIRED_FINITE_FIELDS if not row.get(field)]
    if missing:
        return "REJECT_MISSING_FIELDS", "missing " + ";".join(missing), False
    if row["same_parent_branch_id"] != BRANCH_ID or "MTS" not in row["basis"]:
        return "REJECT_BRANCH_OR_BASIS_MISMATCH", "branch or basis does not match MTS parent WEP basis", False
    value = row["value"].strip()
    bad_tokens = ("MISSING", "PENDING", "PLACEHOLDER", "TEMPLATE")
    if value.startswith(bad_tokens):
        return "REJECT_BAD_VALUE", "value is placeholder/template/missing", False
    if value == "DERIVED_ZERO":
        if row["zero_certificate_status"] != "QT_ZERO_CLOSED" or not is_real_source(row["source_path"]):
            return "REJECT_CLOSURE_ONLY_ZERO", "derived zero lacks parent-signed zero certificate/source", False
    elif not is_finite_numeric(value):
        return "REJECT_BAD_VALUE", "value is neither finite numeric nor DERIVED_ZERO", False
    source_lower = row["source_path"].lower()
    if "microscope" in source_lower and "bound" in source_lower:
        return "REJECT_BAD_PROVENANCE_OR_BOUND_INVERSION", "MICROSCOPE bound cannot be coefficient source", False
    if not is_real_source(row["source_path"]):
        return "REJECT_BAD_PROVENANCE_OR_BOUND_INVERSION", "source_path does not resolve to a source or URL/DOI", False
    if not truthy(row["no_bound_inversion"]) or not truthy(row["no_tau_unity"]):
        return "REJECT_SHORTCUT_POLICY", "no_bound_inversion and no_tau_unity must both be true", False
    if truthy(row["claim_allowed"]):
        return "REJECT_CLAIM_PROMOTION", "finite row may be accepted only as nonclaim quarantine input", False
    return "ACCEPT_SOURCE_PACK_NONCLAIM", f"source-pack row parses under 1603 rules from {rel(path)}", True


def finite_row_search_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, path in enumerate(candidate_paths()):
        exists = path.exists()
        parser_status = "MISSING_LIVE_FILE"
        row_count = 0
        accepted = False
        reason = "candidate path absent"
        if exists:
            try:
                parsed = read_csv(path)
                row_count = len(parsed)
                if parsed:
                    parser_status, reason, accepted = validate_candidate_row(parsed[0], path)
                else:
                    parser_status = "REJECT_EMPTY_CSV"
                    reason = "candidate CSV contains no rows"
            except Exception as exc:
                parser_status = "REJECT_PARSE_ERROR"
                reason = str(exc)
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "search_id": f"FS1604_{index}_{path.stem}",
                "candidate_path": rel(path) if exists else str(path),
                "exists": exists,
                "row_count": row_count,
                "parser_status": parser_status,
                "reason": reason,
                "accepted_for_quarantine": accepted,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    if not rows:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "search_id": "FS1604_NONE",
                "candidate_path": "NO_CANDIDATE_PATHS",
                "exists": False,
                "row_count": 0,
                "parser_status": "NO_FINITE_CEP_CANDIDATE_FOUND",
                "reason": "no candidate files matched finite C_EP source-pack patterns",
                "accepted_for_quarantine": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def validator_dry_run_rows(search_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(search_rows):
        status = row["parser_status"]
        accepted = truthy(row["accepted_for_quarantine"])
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "dry_run_id": f"DRV1604_{index}",
                "candidate_search_id": row["search_id"],
                "validator_basis": "1603 finite C_EP source-pack validator",
                "input_state": status,
                "validator_result": "ACCEPT_NONCLAIM_QUARANTINE" if accepted else status,
                "claim_allowed_after_validation": False,
                "reason": row["reason"],
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "dry_run_id": "DRV1604_POLICY",
            "candidate_search_id": "ALL_CANDIDATES",
            "validator_basis": "anti-circularity policy",
            "input_state": "bound inversion, DD-only proxy, tau_eff=1, template zero, and closure-only zero are forbidden",
            "validator_result": "SHORTCUTS_REJECTED",
            "claim_allowed_after_validation": False,
            "reason": "finite C_EP must be parent-derived or source-backed with units, sign, basis, uncertainty, and provenance",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def runner_rows(search_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted = any(truthy(row["accepted_for_quarantine"]) for row in search_rows)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1604_0_no_wA_zero_route",
            "acceptance_rule": "no-w_A requires parent-signed action-density owner, common measure, typed domain, current owner, no non-Hilbert bypass, and readout no-reentry",
            "input_state": "at least action-density owner/common measure/typed domain/readout clauses remain unsigned",
            "runner_result": "REJECT_NO_WA_THEOREM_ZERO",
            "effect": "C_EP=0 is not certified by source-label forgetting",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1604_1_finite_CEP_route",
            "acceptance_rule": "finite C_EP row must pass source-pack validator and remain nonclaim until WEP gates pass",
            "input_state": "accepted nonclaim row present" if accepted else "no accepted finite C_EP row present",
            "runner_result": "FINITE_ROW_ACCEPTED_NONCLAIM" if accepted else "NO_FINITE_CEP_ROW_ACCEPTED",
            "effect": "finite route is acquisition-ready but not claim-grade",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1604_2_local_arena_policy",
            "acceptance_rule": "WEP/R10/PPN/clock/orbital/local-GR claims require either theorem-zero coupling or complete finite coefficient/source/readout products",
            "input_state": "neither route closed",
            "runner_result": "KEEP_ALL_LOCAL_ARENAS_BLOCKED",
            "effect": "no local-GR or experimental pass is promoted from 1604",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1604_0_no_wA", "no pre-variation source/action weights", "BLOCKED", "parent action-density owner/common measure/domain clauses are unsigned"),
        ("CG1604_1_CEP_zero", "C_EP=0 from source-label forgetting", "BLOCKED", "no-w_A and readout/non-Hilbert clauses remain open"),
        ("CG1604_2_finite_CEP", "finite C_EP source-pack row accepted", "BLOCKED", "no accepted claim-grade finite row exists"),
        ("CG1604_3_WEP", "MICROSCOPE/WEP branch", "BLOCKED", "C_EP and tau/source/readout products are not resolved"),
        ("CG1604_4_local_GR", "derived Newton/GR source normalization", "BLOCKED", "relative source weights cannot yet be killed or bounded"),
        ("CG1604_5_public_claim", "public/local claim", "BLOCKED", "1604 is private gate discipline only"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_rows(search_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted = any(truthy(row["accepted_for_quarantine"]) for row in search_rows)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1604_0_no_wA_route",
            "decision": "NO_WA_THEOREM_NOT_DERIVED",
            "reason": "the direct-sum pre-variation S_matter=sum_A w_A S_A countermodel remains legal until one action-density/measure/domain owner is parent-signed",
            "next_action": "attack the action-density owner/common measure clause directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1604_1_finite_route",
            "decision": "FINITE_CEP_ROW_ACCEPTED_NONCLAIM" if accepted else "FINITE_CEP_ROW_NOT_FOUND_OR_REJECTED",
            "reason": "source-pack validator accepts only real finite/derived-zero rows with provenance; templates and bound inversions remain rejected",
            "next_action": "import-test a real C_EP row only if it supplies value, uncertainty, units, sign, basis, source, no-bound-inversion and no-tau-unity flags",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1604_2_next",
            "decision": "NEXT_1605_ACTION_DENSITY_OWNER_OR_FINITE_CEP_EVIDENCE_IMPORT",
            "reason": "action-density owner is the sharpest theorem route and finite C_EP evidence import is the matching nonzero route",
            "next_action": "prove one shared parent action-density/measure owner forbids independent w_A, or import-test any source-backed finite C_EP evidence row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1605-Y5-R2FR-action-density-owner-or-finite-C_EP-evidence-import.md",
            "script": "scripts/Y5_R2FR_action_density_owner_or_finite_CEP_evidence_import.py",
            "objective": "prove one shared parent action-density/measure owner forbids independent w_A, or import-test any source-backed finite C_EP row",
            "success_condition": "parent-signed action-density owner/common measure theorem closing the pre-variation w_A route, or a validator-readable finite C_EP evidence row that stays nonclaim until WEP gates pass",
            "do_not": "do not use closure-only zero, measured-G absorption, bound inversion, tau_eff=1, DD-only proxy, or public/local-GR claims",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1604() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1604*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    no_wa = read_csv(NO_WA)
    contract = read_csv(ACTION_CONTRACT)
    countermodels = read_csv(COUNTERMODEL)
    search = read_csv(FINITE_SEARCH)
    dry_run = read_csv(VALIDATOR_DRY_RUN)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1604_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1604 local source paths exist"),
        ("VAL1604_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1604 source needles found"),
        ("VAL1604_2_no_wA_verdict", any(row["theorem_id"] == "NWA1604_7_verdict" and row["proof_status"] == "NO_WA_NOT_DERIVED" for row in no_wa), "no-w_A remains a conditional theorem, not a claim"),
        ("VAL1604_3_action_contract", len(contract) >= 5 and all(row["current_status"] != "SIGNED" for row in contract), "parent action-density/measure/domain contract is explicit and unsigned"),
        ("VAL1604_4_countermodel_live", any(row["countermodel_id"] == "WAC1604_0_direct_sum_weight" and row["status"] == "LIVE_COUNTERMODEL" for row in countermodels), "direct-sum w_A countermodel retained"),
        ("VAL1604_5_finite_search_safe", search and all(row["claim_allowed"].lower() == "false" for row in search), "finite C_EP search rows remain nonclaim"),
        ("VAL1604_6_validator_rejects_shortcuts", any(row["validator_result"] == "SHORTCUTS_REJECTED" for row in dry_run), "validator rejects bound inversion, tau_eff=1, DD-only and closure-only shortcuts"),
        ("VAL1604_7_runner_refuses_zero", any(row["runner_id"] == "RUN1604_0_no_wA_zero_route" and row["runner_result"] == "REJECT_NO_WA_THEOREM_ZERO" for row in runner), "runner refuses no-w_A theorem-zero"),
        ("VAL1604_8_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" and row["status"] == "BLOCKED" for row in gates), "all 1604 claim gates remain closed"),
        ("VAL1604_9_decision_next", any(row["decision"] == "NEXT_1605_ACTION_DENSITY_OWNER_OR_FINITE_CEP_EVIDENCE_IMPORT" for row in decisions), "decision selects 1605 action-density owner or finite C_EP import"),
        ("VAL1604_10_csv_parse", csv_parses(generated_csvs), "all generated 1604 CSVs parse"),
        ("VAL1604_11_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1604 rows are score-ready, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1604_12_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1604_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1604_14_formalization_untouched", no_formalization_1604(), "no 1604 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1604_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1604 no-w_A source/action-weight or finite C_EP row-search validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "/")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    no_wa: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    search: list[dict[str, Any]],
    dry_run: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1604 - R2/fR No-w_A Source/Action Weight Or Finite C_EP Row Search",
                "## Verdict\n"
                "- 1604 tries the derivation-first route: prove ordinary matter has no independent pre-variation `w_A S_A` source/action weights.\n"
                "- The useful theorem is exact only as a contract: if one parent action-density/measure/current/domain owner is signed, then relative `w_A` dies modulo a common calibration.\n"
                "- The proof still does not close because `S_matter=sum_A w_A S_A` remains a legal direct-sum countermodel in the current corpus.\n"
                "- The finite `C_EP` search/dry-run found no claim-grade row; templates, bound inversion, `tau_eff=1`, DD-only proxies, and closure-only zero remain rejected.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## No-w_A Theorem Attempt",
                md_table(no_wa, ["theorem_id", "claim_piece", "proof_status", "blocking_gap", "theorem_closed"]),
                "## Source/Action Weight Contract",
                md_table(contract, ["contract_id", "required_parent_signature", "would_prove", "current_status", "acceptance_test"]),
                "## w_A Countermodel Audit",
                md_table(countermodels, ["countermodel_id", "countermodel", "survives_because", "damage_if_live", "status"]),
                "## Finite C_EP Row Search",
                md_table(search, ["search_id", "candidate_path", "exists", "row_count", "parser_status", "accepted_for_quarantine"]),
                "## Finite C_EP Validator Dry Run",
                md_table(dry_run, ["dry_run_id", "candidate_search_id", "input_state", "validator_result", "reason"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "acceptance_rule", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    no_wa = no_wa_rows()
    contract = action_contract_rows()
    countermodels = countermodel_rows()
    search = finite_row_search_rows()
    dry_run = validator_dry_run_rows(search)
    runner = runner_rows(search)
    gates = claim_gate_rows()
    decisions = decision_rows(search)
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        NO_WA,
        ACTION_CONTRACT,
        COUNTERMODEL,
        FINITE_SEARCH,
        VALIDATOR_DRY_RUN,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(NO_WA, no_wa)
    write_csv(ACTION_CONTRACT, contract)
    write_csv(COUNTERMODEL, countermodels)
    write_csv(FINITE_SEARCH, search)
    write_csv(VALIDATOR_DRY_RUN, dry_run)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, no_wa, contract, countermodels, search, dry_run, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
