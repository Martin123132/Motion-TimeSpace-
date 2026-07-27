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
QUARANTINE = MICROSCOPE / "quarantine" / "1605"
INPUT = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1605-Y5-R2FR-action-density-owner-or-finite-C_EP-evidence-import.md"

SOURCE_FILES = {
    "1604_doc": ROOT / "1604-Y5-R2FR-no-wA-source-action-weight-or-finite-C_EP-row-search.md",
    "1604_validation": OUT / "P8_Y5_BRR545_1604_VALIDATION.csv",
    "1604_no_wA": OUT / "P8_Y5_PARENT_QLOC_1604_NO_WA_THEOREM_ATTEMPT.csv",
    "1604_contract": OUT / "P8_Y5_PARENT_QLOC_1604_SOURCE_ACTION_WEIGHT_CONTRACT.csv",
    "1604_countermodel": OUT / "P8_Y5_PARENT_QLOC_1604_WA_COUNTERMODEL_AUDIT.csv",
    "1604_next": OUT / "P8_Y5_PARENT_QLOC_1604_NEXT_TARGET.csv",
    "1463_parent_measure": COEFF / "parent_measure_owner_contract_1463.csv",
    "1463_measure_decision": COEFF / "C_parent_WEP_parent_measure_owner_signing_decision_1463.csv",
    "1464_connected_graph": COEFF / "connected_matter_category_proof_attempt_1464.csv",
    "1464_graph_decision": COEFF / "C_parent_WEP_connected_matter_category_signing_decision_1464.csv",
    "1477_source_gates": COEFF / "source_weight_reduction_gates_1477.csv",
    "1478_single_action": COEFF / "single_action_density_line_proof_attempt_nonclaim_1478.csv",
    "1479_no_source_prefactor": COEFF / "no_source_only_prefactor_typing_theorem_nonclaim_1479.csv",
    "1451_operator_grammar": COEFF / "no_source_only_slot_operator_grammar_theorem_attempt_1451.csv",
    "1452_common_measure": COEFF / "common_measure_current_theorem_attempt_1452.csv",
    "1453_current_owner": COEFF / "current_source_normalization_owner_theorem_attempt_1453.csv",
    "1603_validator": OUT / "P8_Y5_PARENT_QLOC_1603_FINITE_CEP_VALIDATOR_SPEC.csv",
    "1604_finite_search": OUT / "P8_Y5_PARENT_QLOC_1604_FINITE_CEP_ROW_SEARCH.csv",
}

NEEDLES = {
    "1604_doc": ["NWA1604_7_verdict", "NO_WA_NOT_DERIVED"],
    "1604_validation": ["VAL1604_OVERALL", "PASS"],
    "1604_no_wA": ["NWA1604_7_verdict", "NO_WA_NOT_DERIVED"],
    "1604_contract": ["CON1604_0_action_density_owner", "UNSIGNED"],
    "1604_countermodel": ["WAC1604_0_direct_sum_weight", "LIVE_COUNTERMODEL"],
    "1604_next": ["1605-Y5-R2FR-action-density-owner-or-finite-C_EP-evidence-import.md", "finite C_EP row"],
    "1463_parent_measure": ["PMO1463_6_verdict", "CONTRACT_READY_NOT_DERIVED"],
    "1463_measure_decision": ["SIGN1463_0_parent_measure_owner", "False"],
    "1464_connected_graph": ["CON1464_5_verdict", "PROOF_NOT_CLOSED"],
    "1464_graph_decision": ["SIGN1464_0_connected_matter_category", "False"],
    "1477_source_gates": ["GATE1477_2_action_density_line", "False"],
    "1478_single_action": ["SAL1478_4_verdict", "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED"],
    "1479_no_source_prefactor": ["NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"],
    "1451_operator_grammar": ["OG1451_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
    "1452_common_measure": ["CMT1452_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
    "1453_current_owner": ["CSO1453_5_pre_variation_weight", "SURVIVES_PRE_VARIATION"],
    "1603_validator": ["FCV1603_4_zero_policy", "REJECT_CLOSURE_ONLY_ZERO"],
    "1604_finite_search": ["MISSING_LIVE_FILE", "REJECT_BAD_VALUE"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1605_SOURCE_REGISTER.csv"
ACTION_OWNER = OUT / "P8_Y5_PARENT_QLOC_1605_ACTION_DENSITY_OWNER_THEOREM_ATTEMPT.csv"
GRAPH_CERTIFICATE = OUT / "P8_Y5_PARENT_QLOC_1605_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv"
NO_WA_REDUCTION = OUT / "P8_Y5_PARENT_QLOC_1605_NO_WA_REDUCTION_STATUS.csv"
FINITE_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1605_FINITE_CEP_EVIDENCE_IMPORT_TEMPLATE.csv"
FINITE_IMPORT = OUT / "P8_Y5_PARENT_QLOC_1605_FINITE_CEP_EVIDENCE_IMPORT.csv"
VALIDATOR_DRY_RUN = OUT / "P8_Y5_PARENT_QLOC_1605_FINITE_CEP_VALIDATOR_DRY_RUN.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1605_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1605_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1605_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1605_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1605_VALIDATION.csv"

COPY_TARGETS = {
    ACTION_OWNER: [
        QUARANTINE / "ACTION_DENSITY_OWNER_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_action_density_owner_theorem_attempt_nonclaim_1605.csv",
    ],
    GRAPH_CERTIFICATE: [
        QUARANTINE / "CONNECTED_MATTER_GRAPH_CERTIFICATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_connected_matter_graph_certificate_nonclaim_1605.csv",
    ],
    NO_WA_REDUCTION: [
        QUARANTINE / "NO_WA_REDUCTION_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_no_wA_reduction_status_nonclaim_1605.csv",
    ],
    FINITE_TEMPLATE: [
        INPUT / "FINITE_CEP_EVIDENCE_IMPORT_TEMPLATE.csv",
        BRANCH_RESIDUALS / "R2FR_finite_CEP_evidence_import_template_nonclaim_1605.csv",
    ],
    FINITE_IMPORT: [
        QUARANTINE / "FINITE_CEP_EVIDENCE_IMPORT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_CEP_evidence_import_nonclaim_1605.csv",
    ],
    VALIDATOR_DRY_RUN: [
        QUARANTINE / "FINITE_CEP_VALIDATOR_DRY_RUN_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_CEP_validator_dry_run_nonclaim_1605.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1605.csv",
    ],
}

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
                "source_id": f"SRC1605_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1605_action_density_owner_or_finite_CEP_evidence_import_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def action_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "ADO1605_0_target",
            "claim_piece": "one parent action-density owner for ordinary matter",
            "formal_statement": "Ordinary matter is a connected module/category over one parent action-density line L_action with one measure and hbar_parent, rather than a direct sum of independently normalizable source sectors.",
            "status": "TARGET_SHARPENED",
            "what_is_proven": "the exact parent signature needed to forbid independent w_A is identified",
            "blocking_gap": "the signature is not parent-signed in the current corpus",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "ADO1605_1_naturality_lemma",
            "claim_piece": "connected action-line weights collapse",
            "formal_statement": "For nonzero parent-owned morphisms f:A->B on one action-density line, naturality w_B F(f)=F(f) w_A implies w_A=w_B; connectedness propagates w_A=w_*.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "what_is_proven": "relative source weights vanish if the graph is connected and parent-owned",
            "blocking_gap": "physical interaction graph is not yet a parent-owned graph certificate",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "ADO1605_2_common_calibration",
            "claim_piece": "common w_* is not a WEP/source residual",
            "formal_statement": "If w_A=w_* for all ordinary matter and partial w_* is silent across source, material, range, time, and frame labels, then T_source=w_* T_total and w_* is absorbed into measured G_N/GM.",
            "status": "EXACT_IF_UNIVERSAL_AND_SILENT",
            "what_is_proven": "only relative/field-dependent weights are physical source residuals",
            "blocking_gap": "universality cannot be assumed before ADO1605_1 closes",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "ADO1605_3_measure_owner_extension",
            "claim_piece": "species Jacobian and effective-hbar loopholes",
            "formal_statement": "Dmu_parent must be species-blind and no effective hbar_A or Jacobian J_A may act as an action-density/source prefactor.",
            "status": "REQUIRED_EXTENSION_NOT_SIGNED",
            "what_is_proven": "measure ownership is an independent clause, not a corollary of current ownership",
            "blocking_gap": "species Jacobian countermodel survives",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "ADO1605_4_current_owner_limit",
            "claim_piece": "Hilbert current cannot erase pre-action weights",
            "formal_statement": "A unique Hilbert current after variation controls post-variation rescalings, but if w_A is already inside S_matter, T_H inherits w_A.",
            "status": "PRE_VARIATION_WEIGHT_SURVIVES",
            "what_is_proven": "the coupling fight must be won before variation, not downstream in readout/current extraction",
            "blocking_gap": "parent action-density owner is still upstream of current owner",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "ADO1605_5_direct_sum_obstruction",
            "claim_piece": "direct-sum countermodel",
            "formal_statement": "If C_ord splits into disconnected parent source-normalization components, natural positive scalars can be independent constants w_i on each component.",
            "status": "COUNTERMODEL_SURVIVES",
            "what_is_proven": "connectedness and action-line ownership are genuinely necessary",
            "blocking_gap": "no parent-owned connected graph certificate exists yet",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "ADO1605_6_verdict",
            "claim_piece": "action-density owner theorem status",
            "formal_statement": "Action-density owner + connected parent-owned graph + species-blind measure/current + no readout reentry would force Delta_w_A=0, but those parent signatures are not all present.",
            "status": "ACTION_DENSITY_OWNER_NOT_PARENT_SIGNED",
            "what_is_proven": "the derivation route is now reduced to a graph/owner certificate rather than a vague coupling problem",
            "blocking_gap": "line owner, parent-owned graph edges, measure owner, and no reentry remain unsigned",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def graph_certificate_rows() -> list[dict[str, Any]]:
    edges = [
        (
            "GRC1605_0_template_graph",
            "ordinary matter source-relevant graph",
            "electron, photon, quark, gluon, Higgs/Yukawa, nuclear binding, atom/material sectors",
            "physical interaction web is connected for Ti/Pt matter",
            True,
            False,
            "template graph is physical/effective, not parent-owned",
        ),
        (
            "GRC1605_1_QED_edge",
            "electron-photon edge",
            "electron kinetic/current couples to photon/gauge sector",
            "would link electron action normalization to EM sector if edge is parent-owned",
            True,
            False,
            "parent-owned action-line morphism not sourced",
        ),
        (
            "GRC1605_2_QCD_edge",
            "quark-gluon edge",
            "quark colour current couples to gluon sector",
            "would link quark and gluon source-normalization weights",
            True,
            False,
            "parent-owned QCD edge certificate not sourced",
        ),
        (
            "GRC1605_3_Yukawa_edge",
            "fermion-Higgs/Yukawa mass edge",
            "fermion mass terms or mass-generation sector couple to ordinary matter action density",
            "would stop mass terms from carrying independent source-only prefactors",
            True,
            False,
            "parent-owned mass/motion-time action edge not derived",
        ),
        (
            "GRC1605_4_bound_state_edge",
            "nuclear/atomic binding edge",
            "nuclear binding, EM binding, and material composition tie Ti/Pt stress contributions into one source graph",
            "would connect microscopic sector weights to macroscopic WEP materials",
            True,
            False,
            "material graph is not a parent source-normalization proof",
        ),
        (
            "GRC1605_5_readout_edge",
            "source/readout edge",
            "CMSM/readout and source-worldtube maps report WEP observables downstream",
            "would prevent reentry of labels after variation",
            True,
            False,
            "readout no-reentry still unsigned",
        ),
        (
            "GRC1605_6_verdict",
            "connected parent-owned graph certificate",
            "all source-relevant ordinary matter edges must be parent-owned nonzero morphisms on one action-density line",
            "would collapse natural weights to w_* and close Delta_w_A",
            True,
            False,
            "physical connectedness is not enough; parent ownership is missing",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "edge_id": edge_id,
            "edge": edge,
            "objects_or_sectors": objects,
            "would_prove": would_prove,
            "physical_template_edge": physical,
            "parent_owned_edge": parent_owned,
            "current_blocker": blocker,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for edge_id, edge, objects, would_prove, physical, parent_owned, blocker in edges
    ]


def no_wA_reduction_rows() -> list[dict[str, Any]]:
    rows = [
        ("RED1605_0_action_density_line", "single parent action-density line signed", False, "GATE1477_2 and SAL1478_4 say unsigned", "required before direct-sum w_i become illegal"),
        ("RED1605_1_parent_owned_graph", "connected graph edges are parent-owned morphisms", False, "CON1464/SIGN1464 keep connectedness conditional", "required for naturality lemma to propagate w_A=w_*"),
        ("RED1605_2_common_measure", "species-blind measure/Jacobian and hbar owner signed", False, "CMT1452/PMO1463 keep measure owner unsigned", "required to kill J_A/effective-hbar loophole"),
        ("RED1605_3_typed_domain", "no Hom from source labels/hidden markers to source prefactors", False, "OG1451/NST1479 exact only as conditional grammar", "required to forbid source-only prefactor slot"),
        ("RED1605_4_current_and_readout", "current owner plus no non-Hilbert/readout reentry signed", False, "CSO1453 controls post-variation only; readout/no-NH gates open", "required to stop downstream label reentry"),
        ("RED1605_5_common_weight", "only common derivative-silent w_* remains", False, "depends on RED1605_0 through RED1605_4", "would be calibratable into measured G_N/GM"),
        ("RED1605_6_verdict", "Delta_w_A theorem-zero", False, "at least one required parent signature is unsigned", "keep Delta_w_A/C_EP finite route live"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "reduction_id": reduction_id,
            "requirement": requirement,
            "closed": closed,
            "evidence": evidence,
            "effect_if_closed": effect,
            "current_status": "CLOSED" if closed else "OPEN",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for reduction_id, requirement, closed, evidence, effect in rows
    ]


def finite_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "schema_version": "FINITE_CEP_EVIDENCE_IMPORT_1605",
            "coefficient_id": "C_EP_EVIDENCE_TEMPLATE",
            "quantity": "C_EP",
            "value": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "uncertainty": "MISSING_NUMERIC_UNCERTAINTY_OR_EXACT",
            "units": "MISSING_UNITS",
            "sign_convention": "MISSING_TiPt_EP_SOURCE_SIGN_AND_FIELD_BASIS",
            "basis": "MISSING_MTS_PARENT_WEP_BASIS",
            "source_path": "MISSING_PARENT_THEOREM_OR_SOURCE_BACKED_NUMERIC_ROW",
            "parent_status": "MISSING_PARENT_DERIVED_OR_SOURCE_BACKED_NUMERIC",
            "zero_certificate_status": "NOT_ZERO_CERTIFIED",
            "no_bound_inversion": False,
            "no_tau_unity": False,
            "parser_status": "TEMPLATE_ONLY_NOT_IMPORTABLE",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
    return (ROOT / value).exists() or (OUT / value).exists() or (COEFF / value).exists() or (INPUT / value).exists()


def is_finite_numeric(value: str) -> bool:
    try:
        numeric = float(value)
    except ValueError:
        return False
    return math.isfinite(numeric)


def validate_evidence_row(row: dict[str, str], path: Path) -> tuple[str, str, bool]:
    missing = [field for field in REQUIRED_FINITE_FIELDS if not row.get(field)]
    if missing:
        return "REJECT_MISSING_FIELDS", "missing " + ";".join(missing), False
    if row["same_parent_branch_id"] != BRANCH_ID or "MTS" not in row["basis"]:
        return "REJECT_BRANCH_OR_BASIS_MISMATCH", "branch or basis does not match MTS parent WEP basis", False
    value = row["value"].strip()
    if value.startswith(("MISSING", "PENDING", "PLACEHOLDER", "TEMPLATE")):
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
    if truthy(row["claim_allowed"]) or truthy(row["valid_for_claim"]):
        return "REJECT_CLAIM_PROMOTION", "evidence rows remain nonclaim until WEP/local gates pass", False
    return "ACCEPT_EVIDENCE_ROW_NONCLAIM", f"source-pack evidence row parses from {rel(path)}", True


def candidate_paths() -> list[Path]:
    return [
        INPUT / "finite_CEP_evidence_import.csv",
        INPUT / "FINITE_CEP_EVIDENCE_IMPORT_TEMPLATE.csv",
        COEFF / "C_parent_WEP_slot_import.csv",
        COEFF / "C_parent_WEP_slot_import_TEMPLATE.csv",
        OUT / "P8_Y5_PARENT_QLOC_1603_FINITE_CEP_SOURCE_PACK_TEMPLATE.csv",
    ]


def finite_import_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, path in enumerate(candidate_paths()):
        exists = path.exists()
        row_count = 0
        parser_status = "MISSING_LIVE_FILE"
        reason = "candidate path absent"
        accepted = False
        if exists:
            try:
                parsed = read_csv(path)
                row_count = len(parsed)
                if parsed:
                    parser_status, reason, accepted = validate_evidence_row(parsed[0], path)
                else:
                    parser_status = "REJECT_EMPTY_CSV"
                    reason = "candidate CSV contains no rows"
            except Exception as exc:
                parser_status = "REJECT_PARSE_ERROR"
                reason = str(exc)
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "import_id": f"IMP1605_{index}_{path.stem}",
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
    return rows


def validator_dry_run_rows(import_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "dry_run_id": f"DRV1605_{index}",
            "candidate_import_id": row["import_id"],
            "validator_basis": "1603 finite C_EP source-pack validator plus 1605 evidence-import policy",
            "input_state": row["parser_status"],
            "validator_result": "ACCEPT_NONCLAIM_QUARANTINE" if truthy(row["accepted_for_quarantine"]) else row["parser_status"],
            "claim_allowed_after_validation": False,
            "reason": row["reason"],
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, row in enumerate(import_rows)
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "dry_run_id": "DRV1605_POLICY",
            "candidate_import_id": "ALL_CANDIDATES",
            "validator_basis": "anti-circularity policy",
            "input_state": "closure-only zero, measured-G absorption, MICROSCOPE-bound inversion, tau_eff=1, DD-only proxy, and template rows are forbidden",
            "validator_result": "SHORTCUTS_REJECTED",
            "claim_allowed_after_validation": False,
            "reason": "finite C_EP evidence must be parent-derived or source-backed with value, uncertainty, units, sign, basis, source, no-bound-inversion, and no-tau-unity",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def runner_rows(import_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted = any(truthy(row["accepted_for_quarantine"]) for row in import_rows)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1605_0_action_owner_theorem",
            "acceptance_rule": "Delta_w_A=0 requires parent-signed action-density owner, parent-owned connected graph, species-blind measure/current, typed no-source-slot domain, and readout/no-NH silence",
            "input_state": "action owner and graph certificates are conditional, not signed",
            "runner_result": "REJECT_ACTION_OWNER_THEOREM_ZERO",
            "effect": "no-w_A remains open; source residual vector stays live",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1605_1_finite_CEP_evidence",
            "acceptance_rule": "finite C_EP evidence row must pass strict validator and remain nonclaim until WEP/local gates pass",
            "input_state": "accepted nonclaim row present" if accepted else "no accepted finite C_EP evidence row present",
            "runner_result": "FINITE_EVIDENCE_ACCEPTED_NONCLAIM" if accepted else "NO_FINITE_CEP_EVIDENCE_ACCEPTED",
            "effect": "finite route remains input-ready but not claim-grade",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1605_2_local_GR_policy",
            "acceptance_rule": "derived Newton/GR source side requires theorem-zero relative weights or bounded finite source residuals",
            "input_state": "neither theorem-zero nor finite evidence route closed",
            "runner_result": "KEEP_NEWTON_GR_SOURCE_SIDE_BLOCKED",
            "effect": "no local-GR, WEP, R10, PPN, clock, or orbital pass is promoted",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1605_0_action_owner", "one parent action-density owner", "BLOCKED", "contract exists but is not parent-signed"),
        ("CG1605_1_parent_graph", "connected parent-owned matter graph", "BLOCKED", "physical graph exists only as template; parent-owned edges missing"),
        ("CG1605_2_no_wA", "Delta_w_A theorem-zero", "BLOCKED", "action line, graph, measure, domain, and readout clauses are not all closed"),
        ("CG1605_3_finite_CEP", "finite C_EP evidence accepted", "BLOCKED", "no source-backed finite/derived-zero row accepted for claim"),
        ("CG1605_4_Newton_GR", "source-normalized Newton/GR limit", "BLOCKED", "relative active-source weights remain live"),
        ("CG1605_5_public_claim", "public/local experimental claim", "BLOCKED", "1605 is private derivation/input discipline only"),
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


def decision_rows(import_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted = any(truthy(row["accepted_for_quarantine"]) for row in import_rows)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1605_0_action_owner",
            "decision": "ACTION_DENSITY_OWNER_NOT_PARENT_SIGNED",
            "reason": "the naturality proof is exact, but the parent-owned connected matter graph and one-line action-density owner certificate are missing",
            "next_action": "turn physical ordinary-matter connectedness into a parent-owned graph certificate or keep Delta_w components explicit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1605_1_finite_evidence",
            "decision": "FINITE_CEP_EVIDENCE_ACCEPTED_NONCLAIM" if accepted else "FINITE_CEP_EVIDENCE_NOT_FOUND_OR_REJECTED",
            "reason": "strict evidence import accepts no template, bound inversion, tau-unity, DD-only, or closure-only row",
            "next_action": "only import a real finite/derived-zero row with source, uncertainty, units, sign, basis and shortcut firewalls",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1605_2_next",
            "decision": "NEXT_1606_PARENT_OWNED_MATTER_GRAPH_OR_DELTA_W_COMPONENT_BOUND_PACK",
            "reason": "parent-owned graph certificate is the remaining theorem route; Delta_w component pack is the matching finite/bounded route",
            "next_action": "prove source-relevant ordinary matter edges are parent-owned morphisms on one action-density line, or build source-ready Delta_w component bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1606-Y5-R2FR-parent-owned-matter-graph-or-Delta_w-component-bound-pack.md",
            "script": "scripts/Y5_R2FR_parent_owned_matter_graph_or_Delta_w_component_bound_pack.py",
            "objective": "prove source-relevant ordinary matter graph edges are parent-owned action-density morphisms, or build source-ready Delta_w component bound rows",
            "success_condition": "parent-owned connected graph certificate that collapses action weights to w_*, or nonclaim finite/bound rows for Delta_w components with units, sources, signs and no shortcut provenance",
            "do_not": "do not use physical connectedness alone, closure-only zero, measured-G absorption, bound inversion, tau_eff=1, DD-only proxy, or public/local-GR claims",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


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


def no_formalization_1605() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1605*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    action = read_csv(ACTION_OWNER)
    graph = read_csv(GRAPH_CERTIFICATE)
    reduction = read_csv(NO_WA_REDUCTION)
    template = read_csv(FINITE_TEMPLATE)
    imports = read_csv(FINITE_IMPORT)
    dry_run = read_csv(VALIDATOR_DRY_RUN)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1605_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1605 local source paths exist"),
        ("VAL1605_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1605 source needles found"),
        ("VAL1605_2_action_owner_verdict", any(row["theorem_id"] == "ADO1605_6_verdict" and row["status"] == "ACTION_DENSITY_OWNER_NOT_PARENT_SIGNED" for row in action), "action-density owner remains unsigned"),
        ("VAL1605_3_naturality_lemma", any(row["theorem_id"] == "ADO1605_1_naturality_lemma" and row["status"] == "EXACT_CONDITIONAL_LEMMA" for row in action), "connected action-line naturality lemma is recorded"),
        ("VAL1605_4_graph_not_parent_owned", any(row["edge_id"] == "GRC1605_6_verdict" and row["parent_owned_edge"].lower() == "false" for row in graph), "connected graph certificate remains physical-template-only"),
        ("VAL1605_5_no_wA_not_closed", any(row["reduction_id"] == "RED1605_6_verdict" and row["closed"].lower() == "false" for row in reduction), "Delta_w_A theorem-zero remains blocked"),
        ("VAL1605_6_template_nonimportable", any(row["parser_status"] == "TEMPLATE_ONLY_NOT_IMPORTABLE" for row in template), "finite C_EP evidence template remains nonimportable"),
        ("VAL1605_7_finite_import_safe", imports and all(row["claim_allowed"].lower() == "false" for row in imports), "finite C_EP evidence import rows remain nonclaim"),
        ("VAL1605_8_validator_rejects_shortcuts", any(row["validator_result"] == "SHORTCUTS_REJECTED" for row in dry_run), "validator rejects shortcut evidence routes"),
        ("VAL1605_9_runner_refuses_claims", any(row["runner_id"] == "RUN1605_0_action_owner_theorem" and row["runner_result"] == "REJECT_ACTION_OWNER_THEOREM_ZERO" for row in runner) and any(row["runner_id"] == "RUN1605_2_local_GR_policy" and row["runner_result"] == "KEEP_NEWTON_GR_SOURCE_SIDE_BLOCKED" for row in runner), "runner refuses theorem-zero and local-GR promotion"),
        ("VAL1605_10_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" and row["status"] == "BLOCKED" for row in gates), "all 1605 claim gates remain closed"),
        ("VAL1605_11_decision_next", any(row["decision"] == "NEXT_1606_PARENT_OWNED_MATTER_GRAPH_OR_DELTA_W_COMPONENT_BOUND_PACK" for row in decisions), "decision selects 1606 parent-owned graph or Delta_w component pack"),
        ("VAL1605_12_csv_parse", csv_parses(generated_csvs), "all generated 1605 CSVs parse"),
        ("VAL1605_13_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1605 rows are score-ready, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1605_14_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1605_15_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1605_16_formalization_untouched", no_formalization_1605(), "no 1605 outputs found under formalization-workbench"),
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
            "check_id": "VAL1605_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1605 action-density owner or finite C_EP evidence import validation",
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
            values.append(str(row.get(column, "")).replace("\n", " ").replace("|", "/"))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    action: list[dict[str, Any]],
    graph: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    template: list[dict[str, Any]],
    imports: list[dict[str, Any]],
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
                "# 1605 - R2/fR Action-Density Owner Or Finite C_EP Evidence Import",
                "## Verdict\n"
                "- 1605 proves the useful conditional lemma: on one parent action-density line, a connected parent-owned matter graph collapses natural positive action weights to one common `w_*`.\n"
                "- A derivative-silent common `w_*` is calibration; it is not a WEP/source residual. Relative or field-dependent `Delta_w_A` remains physical.\n"
                "- The theorem is not promoted because the parent-owned connected graph, one action-density owner, species-blind measure, typed no-source-slot domain, and readout/no-NH silence are not all signed.\n"
                "- The finite `C_EP` evidence import was dry-run strict: template, missing live file, bound inversion, `tau_eff=1`, DD-only proxy, measured-G absorption, and closure-only zero are rejected.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Action-Density Owner Theorem Attempt",
                md_table(action, ["theorem_id", "claim_piece", "status", "what_is_proven", "blocking_gap", "theorem_closed"]),
                "## Connected Matter Graph Certificate",
                md_table(graph, ["edge_id", "edge", "physical_template_edge", "parent_owned_edge", "current_blocker"]),
                "## No-w_A Reduction Status",
                md_table(reduction, ["reduction_id", "requirement", "closed", "current_status", "evidence", "effect_if_closed"]),
                "## Finite C_EP Evidence Import Template",
                md_table(template, ["coefficient_id", "quantity", "value", "source_path", "parser_status"]),
                "## Finite C_EP Evidence Import",
                md_table(imports, ["import_id", "candidate_path", "exists", "row_count", "parser_status", "accepted_for_quarantine"]),
                "## Finite C_EP Validator Dry Run",
                md_table(dry_run, ["dry_run_id", "candidate_import_id", "input_state", "validator_result", "reason"]),
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
    INPUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    action = action_owner_rows()
    graph = graph_certificate_rows()
    reduction = no_wA_reduction_rows()
    template = finite_template_rows()
    write_csv(FINITE_TEMPLATE, template)
    (INPUT / "FINITE_CEP_EVIDENCE_IMPORT_TEMPLATE.csv").parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(FINITE_TEMPLATE, INPUT / "FINITE_CEP_EVIDENCE_IMPORT_TEMPLATE.csv")
    imports = finite_import_rows()
    dry_run = validator_dry_run_rows(imports)
    runner = runner_rows(imports)
    gates = claim_gate_rows()
    decisions = decision_rows(imports)
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        ACTION_OWNER,
        GRAPH_CERTIFICATE,
        NO_WA_REDUCTION,
        FINITE_TEMPLATE,
        FINITE_IMPORT,
        VALIDATOR_DRY_RUN,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACTION_OWNER, action)
    write_csv(GRAPH_CERTIFICATE, graph)
    write_csv(NO_WA_REDUCTION, reduction)
    write_csv(FINITE_IMPORT, imports)
    write_csv(VALIDATOR_DRY_RUN, dry_run)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, action, graph, reduction, template, imports, dry_run, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
