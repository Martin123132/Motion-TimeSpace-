from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1838"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1838-Y5-R2FR-ordinary-matter-action-signature-source-label-forgetting-or-WEP-bound-first-fill.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1838_0_1837_next",
        "source_key": "1837_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_NEXT_TARGET.csv",
        "needles": ["NEXT1837_0_primary", "selected"],
        "role": "1837 selects ordinary matter action signature/source-label forgetting or WEP first bound fill.",
    },
    {
        "source_id": "SRC1838_1_1837_validation",
        "source_key": "1837_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1837_VALIDATION.csv",
        "needles": ["VAL1837_OVERALL", "PASS"],
        "role": "confirms 1837 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1838_2_1837_component_bound",
        "source_key": "1837_WEP_component_bound_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1837_WEP_COMPONENT_BOUND_ROWS.csv",
        "needles": ["WCB1837_1_material_source_weight", "MISSING_DELTA_W_AND_TAU_WEP"],
        "role": "points to the first material/source-weight WEP component bound row.",
    },
    {
        "source_id": "SRC1838_3_1088_MOMS",
        "source_key": "1088_MOMS_signature",
        "source_path": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
        "needles": ["MOMS1088_7_verdict", "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED"],
        "role": "minimal ordinary matter signature is exact but unsigned.",
    },
    {
        "source_id": "SRC1838_4_1090_axioms",
        "source_key": "1090_MOMS_synthesis",
        "source_path": ROOT / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md",
        "needles": ["AX1090_0_parent_object", "SYNTHESIS_FAILS_MISSING_AXIOMS"],
        "role": "MOMS synthesis fails without five missing parent axioms.",
    },
    {
        "source_id": "SRC1838_5_1476_source_label",
        "source_key": "1476_source_label_forgetting",
        "source_path": ROOT / "1476-Y5-R10-RAB-source-label-forgetting-proof-or-Ci-source-weight-numeric-row.md",
        "needles": ["SLF1476_4_verdict", "NOT_PARENT_DERIVED_EMIT_DELTA_W_INPUT_ROW"],
        "role": "source-label forgetting is exact conditional and emits Delta_w input rows.",
    },
    {
        "source_id": "SRC1838_6_1479_no_prefactor",
        "source_key": "1479_no_source_only_prefactor",
        "source_path": ROOT / "1479-Y5-R10-RAB-no-source-only-action-prefactor-typing-theorem-or-delta-w-bound-pack.md",
        "needles": ["NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"],
        "role": "no-source-only prefactor theorem remains a conditional typing theorem.",
    },
    {
        "source_id": "SRC1838_7_1766_exchange_graph",
        "source_key": "1766_exchange_graph",
        "source_path": ROOT / "1766-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md",
        "needles": ["OMC1766_1_connected_graph_implication", "CONDITIONAL_ORDINARY_BLOCK_ZERO_PARENT_UNSIGNED"],
        "role": "connected ordinary exchange graph narrows the remaining problem to source shadow and sourced graph rows.",
    },
    {
        "source_id": "SRC1838_8_1686_label_quotient",
        "source_key": "1686_parent_label_quotient",
        "source_path": MICROSCOPE_RESIDUALS / "R2FR_parent_label_quotient_clause_audit_1686.csv",
        "needles": ["PLQ1686_6_verdict", "PROOF_NOT_CLOSED"],
        "role": "parent label quotient clauses are exact but not parent-signed.",
    },
    {
        "source_id": "SRC1838_9_1630_AX1090",
        "source_key": "1630_AX1090_status",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1630_AX1090_REDUCTION_STATUS.csv",
        "needles": ["AX1630_5_verdict", "AX1090_BUNDLE_NOT_REDUCED"],
        "role": "AX1090 bundle remains unreduced to MTS primitives.",
    },
    {
        "source_id": "SRC1838_10_1476_delta_w",
        "source_key": "1476_delta_w_input",
        "source_path": MICROSCOPE / "quarantine" / "1476" / "DELTA_W_SOURCE_WEIGHT_INPUT_ROW_NONCLAIM.csv",
        "needles": ["DW1476_0_delta_w_A", "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W"],
        "role": "existing Delta_w input row supplies the first nonclaim WEP bound input shape.",
    },
    {
        "source_id": "SRC1838_11_1067_tau_WEP",
        "source_key": "1067_tau_WEP_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv",
        "needles": ["TAQ1067_2_delta_w_width_if_tau", "MISSING_TAU_WEP"],
        "role": "tau_WEP/direct product is still missing before Delta_w can be turned into an eta width.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1838_SOURCE_REGISTER.csv",
    "ordinary_matter_signature_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1838_ORDINARY_MATTER_SIGNATURE_AUDIT.csv",
    "source_label_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1838_SOURCE_LABEL_FORGETTING_GATE.csv",
    "first_WEP_component_bound_input": RESIDUALS / "P8_Y5_PARENT_QLOC_1838_FIRST_WEP_COMPONENT_BOUND_INPUT.csv",
    "current_corpus_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1838_CURRENT_CORPUS_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1838_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1838_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1838_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing_needles = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing_needles,
                "missing_needles": ";".join(missing_needles),
                "role": source["role"],
            }
        )
    return rows


def ordinary_matter_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OMS1838_0_action_form",
            "required_statement": "S_ord = sum_A S_A[Psi_A; E(q(Phi)), Omega(E(q(Phi))), A_obs(q(Phi)), theta_A] with no hidden representative/source-only argument.",
            "if_signed": "ordinary matter sees only quotient-owned observed geometry/gauge data and fixed representation constants",
            "current_status": "EXACT_CONTRACT_NOT_PARENT_DERIVED",
            "blocks": "P_WEP zero theorem; qbar_source_weight zero; local WEP promotion",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OMS1838_1_parent_object",
            "required_statement": "one parent action object owns ordinary matter before all readout/projection/fitting choices",
            "if_signed": "prevents stitching separate contracts into a fake derivation",
            "current_status": "PARENT_OBJECT_NOT_PROVEN",
            "blocks": "MOMS adoption as theorem",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OMS1838_2_matter_bundle",
            "required_statement": "ordinary matter fields are sections over the observed quotient bundle, with vertical lifts only gauge/boundary/local-Lorentz/diffeomorphism",
            "if_signed": "no physical ordinary-matter lift along quotient-vertical directions",
            "current_status": "MISSING_PARENT_MATTER_BUNDLE_FUNCTOR",
            "blocks": "matter descent",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OMS1838_3_constant_superselection",
            "required_statement": "masses, charges, alpha_EM, clock standards, representation labels and hbar/c are q-owned fixed data or retained residual fields",
            "if_signed": "removes hidden material/constant WEP currents",
            "current_status": "CONSTANT_SECTOR_UNSIGNED",
            "blocks": "composition source-current zero",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OMS1838_4_no_species_weights",
            "required_statement": "no independent w_A(X) S_A, kappa_A T_A, source-only material multiplier, or species-label scalar is an allowed parent argument",
            "if_signed": "Delta_w_TiPt is syntactically impossible before variation",
            "current_status": "SOURCE_ONLY_WEIGHT_EXCLUSION_UNSIGNED",
            "blocks": "WEP material/source row",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OMS1838_5_variation_order",
            "required_statement": "Hilbert/current extraction occurs before material projection, empirical readout, source-worldtube selection, or calibration",
            "if_signed": "post-variation source selectors cannot manufacture a WEP residual",
            "current_status": "CONDITIONAL_SUBTHEOREM_ONLY",
            "blocks": "readout no-reentry",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OMS1838_6_no_shadow_domain",
            "required_statement": "no shadow source map, matter frame, domain marker, boundary charge, or support/readout marker reintroduces species labels",
            "if_signed": "source-shadow route is eliminated",
            "current_status": "SOURCE_SHADOW_BAN_UNSIGNED",
            "blocks": "local WEP/Newton/PPN transfer",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OMS1838_7_verdict",
            "required_statement": "OMS1838_0 through OMS1838_6 are all parent-signed in one action",
            "if_signed": "P_WEP material/source branch is theorem-zero",
            "current_status": "ORDINARY_MATTER_SIGNATURE_NOT_PARENT_SIGNED",
            "blocks": "P_WEP=0 and local-GR promotion",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def source_label_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SLG1838_0_total_Hilbert_source",
            "claim_piece": "source functor domain is total Hilbert stress/current",
            "formal_statement": "q_src({(T_A,A)}) = sum_A T_A before gravitational source selection",
            "current_result": "EXACT_CONDITIONAL_THEOREM",
            "countermodel": "F((T_A,A)) = sum_A kappa_A T_A remains covariant/additive if labels survive",
            "passes_current_corpus": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SLG1838_1_connected_exchange_graph",
            "claim_piece": "ordinary matter exchange graph collapses weights",
            "formal_statement": "if G_ord is connected and weights are natural on exchange morphisms, all w_A=w_*",
            "current_result": "DERIVED_CONDITIONAL_THEOREM_SOURCE_CERT_MISSING",
            "countermodel": "disconnected source-relevant components can carry independent weights",
            "passes_current_corpus": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SLG1838_2_common_measure_current",
            "claim_piece": "one action measure/current owner",
            "formal_statement": "S_ord/hbar_parent has one action scale, species-blind measure/Jacobian, and one Hilbert/coframe current owner",
            "current_result": "MISSING_AXIOM_NOT_REDUCED",
            "countermodel": "w_A S_A or species-dependent Jacobian changes Hilbert source while preserving isolated EOM form",
            "passes_current_corpus": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SLG1838_3_no_hidden_hom",
            "claim_piece": "no hidden-visible coefficient map",
            "formal_statement": "Hom(hidden/representative/marker, active-source-prefactor) is absent except through q-owned fixed data",
            "current_result": "NO_HOM_CONTRACT_NOT_PARENT_DERIVED",
            "countermodel": "hidden invariant, marker, readout or current map supplies a finite source prefactor",
            "passes_current_corpus": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SLG1838_4_readout_no_reentry",
            "claim_piece": "readout/source-worldtube maps preserve label forgetting",
            "formal_statement": "K_readout o q_src has no species-label argument except through the already-summed T_total",
            "current_result": "READOUT_TRANSFER_UNSIGNED",
            "countermodel": "source-worldtube/readout kernel recreates effective source labels after variation",
            "passes_current_corpus": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SLG1838_5_verdict",
            "claim_piece": "source-label forgetting signs Delta_w_TiPt=0",
            "formal_statement": "SLG1838_0 through SLG1838_4 all parent-signed",
            "current_result": "SOURCE_LABEL_FORGETTING_NOT_DERIVED",
            "countermodel": "relative source-weight/source-shadow countermodels remain legal",
            "passes_current_corpus": False,
            "valid_for_claim": False,
        },
    ]


def first_WEP_component_bound_rows() -> list[dict[str, Any]]:
    tau_source = RESIDUALS / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv"
    delta_w_source = MICROSCOPE / "quarantine" / "1476" / "DELTA_W_SOURCE_WEIGHT_INPUT_ROW_NONCLAIM.csv"
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "FWCB1838_0_delta_w_TiPt",
            "quantity": "Delta_w_TiPt",
            "definition": "relative ordinary-matter source/action weight for Ti/Pt after removing any common calibration",
            "formula": "q_source^nu = P_loc nabla_mu[Delta_w_TiPt T_TiPt^{mu nu}] + boundary/projector/readout terms",
            "accepted_evidence": "parent theorem-zero certificate OR numeric/source-backed Delta_w_TiPt with units, sign convention, source anchor and no-cancellation statement",
            "current_value": "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W",
            "units": "dimensionless source/action weight",
            "bound_or_gate": "if tau_WEP numeric and nonzero, abs(Delta_w_TiPt) <= 2.8e-15/abs(tau_WEP); otherwise use direct product evaluator",
            "source_artifact": str(delta_w_source),
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "passes_required_gate": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "FWCB1838_1_tau_WEP",
            "quantity": "tau_WEP",
            "definition": "normalized local source/orbit/readout projection converting Delta_w_TiPt into a WEP eta residual",
            "formula": "eta_material_TiPt = Delta_w_TiPt * tau_WEP",
            "accepted_evidence": "parent theorem-zero WEP projection OR numeric local source/orbit/readout integral",
            "current_value": "MISSING_TAU_WEP",
            "units": "dimensionless projection factor",
            "bound_or_gate": "required before converting eta bound into Delta_w width",
            "source_artifact": str(tau_source),
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "passes_required_gate": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "FWCB1838_2_direct_product",
            "quantity": "P_WEP_material_direct",
            "definition": "unsplit parent product from material/source-weight branch to eta_TiPt",
            "formula": "eta_material_TiPt = P_WEP_material · DeltaGamma_material",
            "accepted_evidence": "derived parent product or sourced numeric product with same branch lock",
            "current_value": "MISSING_DIRECT_PRODUCT",
            "units": "dimensionless eta contribution",
            "bound_or_gate": "alternative to splitting Delta_w_TiPt and tau_WEP",
            "source_artifact": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1837_PWEP_RESPONSE_CONTRACT.csv"),
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "passes_required_gate": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "FWCB1838_3_width_rule",
            "quantity": "Delta_w_TiPt_width",
            "definition": "nonclaim prior-width rule if tau_WEP becomes numeric and nonzero",
            "formula": "abs(Delta_w_TiPt)_max = 2.8e-15 / abs(tau_WEP)",
            "accepted_evidence": "tau_WEP numeric plus MICROSCOPE bound convention and no measured-G absorption",
            "current_value": "NOT_EVALUATED_TAU_WEP_MISSING",
            "units": "dimensionless",
            "bound_or_gate": "width rule only; not a prediction",
            "source_artifact": str(tau_source),
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "passes_required_gate": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "FWCB1838_4_refusal_guard",
            "quantity": "WEP_material_row_guard",
            "definition": "anti-shortcut rule for the first WEP component row",
            "formula": "reject tau_WEP=1 shortcuts, measured-G absorption, cancellation, surrogate arrays, and branch mixing",
            "accepted_evidence": "branch-locked sourced rows only",
            "current_value": "REFUSAL_ACTIVE",
            "units": "not_applicable",
            "bound_or_gate": "blocks false positives",
            "source_artifact": str(MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv"),
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "passes_required_gate": False,
            "valid_for_claim": False,
        },
    ]


def current_corpus_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1838_0_MOMS_signature",
            "claim": "ordinary matter action signature is parent-signed",
            "gate_pass": False,
            "reason": "1088/1090/1630 leave MOMS/AX1090 as exact contract or missing-axiom bundle",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1838_1_source_label_forgetting",
            "claim": "Delta_w_TiPt=0 by source-label forgetting",
            "gate_pass": False,
            "reason": "1476/1686 keep parent label quotient/source functor unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1838_2_connected_graph",
            "claim": "ordinary graph connectivity currently proves WEP material-source zero",
            "gate_pass": False,
            "reason": "1766 conditionally narrows the block but still needs source-backed graph certificate and source-shadow ban",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1838_3_first_component_input",
            "claim": "first WEP material/source component is score-ready",
            "gate_pass": False,
            "reason": "Delta_w_TiPt, tau_WEP and direct product are still missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1838_4_current_WEP",
            "claim": "WEP/local-GR route is promoted",
            "gate_pass": False,
            "reason": "the route is sharpened but remains nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1838_0_signature_attempt",
            "decision": "ORDINARY_MATTER_SIGNATURE_NOT_PARENT_SIGNED",
            "reason": "MOMS/AX1090 clauses are exact but remain missing parent axioms, not current derivations",
            "next_action": "do not set Delta_w_TiPt=0",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1838_1_first_bound_row",
            "decision": "FIRST_WEP_MATERIAL_SOURCE_BOUND_INPUT_FILLED_NONCLAIM",
            "reason": "Delta_w_TiPt and tau_WEP/direct product are now explicit row requirements with refusal guards",
            "next_action": "either prove source-shadow ban or source tau_WEP/direct product",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1838_2_best_next",
            "decision": "SOURCE_SHADOW_BAN_OR_TAUWEP_DIRECT_PRODUCT_NEXT",
            "reason": "after connected ordinary matter, the cleanest bypass is a shadow source map or readout projector that recreates labels",
            "next_action": "1839-Y5-R2FR-source-shadow-ban-or-tauWEP-direct-product-first-source-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1838_0_primary",
            "next_target": "1839-Y5-R2FR-source-shadow-ban-or-tauWEP-direct-product-first-source-row.md",
            "script": "scripts/Y5_R2FR_source_shadow_ban_or_tauWEP_direct_product_first_source_row.py",
            "objective": "try to prove the source map is only the total Hilbert source with no shadow/readout label re-entry; if it fails, fill the tau_WEP/direct product first source row as nonclaim",
            "selection_status": "selected",
            "success_condition": "source-shadow is parent-forbidden, or tau_WEP/direct-product acquisition is explicit and still nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1838_1_fallback",
            "next_target": "1839b-Y5-R2FR-standard-matter-graph-source-certificate.md",
            "script": "scripts/Y5_R2FR_standard_matter_graph_source_certificate.py",
            "objective": "source the ordinary exchange graph edges and arena exclusions needed by the connected-graph conditional theorem",
            "selection_status": "held_fallback",
            "success_condition": "graph certificate is source-backed without claiming WEP unless source-shadow is also closed",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "ordinary_matter_signature_audit": ordinary_matter_signature_rows(),
        "source_label_gate": source_label_gate_rows(),
        "first_WEP_component_bound_input": first_WEP_component_bound_rows(),
        "current_corpus_gate": current_corpus_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_csvs(paths: list[Path]) -> None:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            directory.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, directory / path.name)


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open("r", encoding="utf-8", newline="") as handle:
                list(csv.DictReader(handle))
    except Exception:
        return False
    return True


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    guarded_keys = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "parent_signed", "passes_required_gate", "numeric_input_present", "theorem_zero_present"}
    for rows in rows_map.values():
        for row in rows:
            for guarded_key in guarded_keys.intersection(row):
                if str(row[guarded_key]).lower() == "true":
                    return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if "1838-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1838") or name.startswith("P8_Y5_BRR545_1838"):
            return False
    return True


def branch_copies_exist(paths: list[Path]) -> bool:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            if not (directory / path.name).exists():
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]], copied_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    output_paths = [OUTPUTS[key] for key in rows_map.keys()]
    signature_rows = rows_map["ordinary_matter_signature_audit"]
    label_rows = rows_map["source_label_gate"]
    input_rows = rows_map["first_WEP_component_bound_input"]
    gate_rows = rows_map["current_corpus_gate"]
    checks: list[tuple[str, bool, str]] = [
        ("VAL1838_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1838_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL1838_2_signature_verdict_nonclaim",
            any(row["clause_id"] == "OMS1838_7_verdict" and row["current_status"] == "ORDINARY_MATTER_SIGNATURE_NOT_PARENT_SIGNED" for row in signature_rows),
            "ordinary matter signature remains unsigned",
        ),
        (
            "VAL1838_3_source_label_gate_refused",
            any(row["gate_id"] == "SLG1838_5_verdict" and row["current_result"] == "SOURCE_LABEL_FORGETTING_NOT_DERIVED" for row in label_rows),
            "source-label forgetting is not promoted",
        ),
        (
            "VAL1838_4_first_WEP_input_rows",
            {"FWCB1838_0_delta_w_TiPt", "FWCB1838_1_tau_WEP", "FWCB1838_2_direct_product"}.issubset({row["input_id"] for row in input_rows}),
            "Delta_w, tau_WEP and direct-product input rows are present",
        ),
        (
            "VAL1838_5_first_WEP_inputs_nonclaim",
            all(row["valid_for_claim"] is False and row["passes_required_gate"] is False for row in input_rows),
            "all first WEP component inputs remain nonclaim and failing",
        ),
        (
            "VAL1838_6_current_gate_blocks_WEP",
            any(row["gate_id"] == "CG1838_4_current_WEP" and row["gate_pass"] is False for row in gate_rows),
            "current WEP/local-GR promotion is blocked",
        ),
        (
            "VAL1838_7_next_selected",
            any(row["route_id"] == "NEXT1838_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selects source-shadow ban or tau_WEP direct product",
        ),
        ("VAL1838_8_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1838_9_csv_parse", csv_parse_ok(output_paths), "all generated 1838 CSVs parse"),
        ("VAL1838_10_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1838_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1838_12_formalization_untouched", no_formalization_outputs(), "no 1838 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1838_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1838 ordinary matter action signature/source-label forgetting or WEP first-bound fill checkpoint",
        }
    )
    return rows


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1838 Y5 R2FR ordinary matter action signature source-label forgetting or WEP bound first fill",
            "",
            "**Progress:** 1838 consolidates the ordinary-matter signature route. The result is sharp: if one parent ordinary-matter action owns the observed geometry, constants, measure/current and variation-before-readout rules, then the WEP material/source branch is theorem-zero. Current files do not sign that, so the first `Delta_w_TiPt` WEP input row is filled as nonclaim instead.",
            "",
            "**Current verdict:** the ordinary-matter action signature and source-label forgetting route remain conditional. `Delta_w_TiPt`, `tau_WEP`, and the direct material/source product are explicit missing inputs; no WEP or local-GR claim is allowed.",
            "",
            "**Claim ceiling:** no ordinary-matter signature claim, no `Delta_w_TiPt=0` claim, no WEP score, no tau shortcut, no measured-G absorption, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1838.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Ordinary Matter Signature Audit",
            markdown_table(rows_map["ordinary_matter_signature_audit"], ["clause_id", "required_statement", "if_signed", "current_status", "blocks", "parent_signed", "valid_for_claim"]),
            "",
            "## Source-Label Forgetting Gate",
            markdown_table(rows_map["source_label_gate"], ["gate_id", "claim_piece", "formal_statement", "current_result", "countermodel", "passes_current_corpus", "valid_for_claim"]),
            "",
            "## First WEP Component Bound Input",
            markdown_table(rows_map["first_WEP_component_bound_input"], ["input_id", "quantity", "definition", "formula", "accepted_evidence", "current_value", "units", "bound_or_gate", "source_artifact", "passes_required_gate", "valid_for_claim"]),
            "",
            "## Current Corpus Gate",
            markdown_table(rows_map["current_corpus_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is progress in the boxing-match sense: we did not land the knockout, but we took away a lot of room for the opponent to hide. Ordinary connected matter wants one common Hilbert source. The main remaining escape hatch is a shadow source/readout map that reintroduces labels after variation. That is now the next target.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    nonvalidation_paths: list[Path] = []
    for key, rows in rows_map.items():
        path = OUTPUTS[key]
        write_csv(path, rows)
        nonvalidation_paths.append(path)
    copy_csvs(nonvalidation_paths)
    validation_rows = build_validation(rows_map, nonvalidation_paths)
    write_csv(OUTPUTS["validation"], validation_rows)
    copy_csvs([OUTPUTS["validation"]])
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1838 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
