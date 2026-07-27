from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3084"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3084-Y5-R2FR-ordinary-matter-action-signature-source-label-forgetting-or-WEP-bound-first-fill-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3084_00_3083_doc": ROOT / "3083-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-under-AX1090.md",
    "SRC3084_01_3083_next": RESIDUALS / "P8_Y5_R2FR_3083_NEXT_TARGET.csv",
    "SRC3084_02_3083_derivation": RESIDUALS / "P8_Y5_R2FR_3083_PWEP_DERIVATION_ATTEMPT.csv",
    "SRC3084_03_3083_gate": RESIDUALS / "P8_Y5_R2FR_3083_CURRENT_CORPUS_GATE.csv",
    "SRC3084_04_3083_dependency": RESIDUALS / "P8_Y5_R2FR_3083_PARENT_SIGNATURE_DEPENDENCY_LADDER.csv",
    "SRC3084_05_3083_wep_bounds": RESIDUALS / "P8_Y5_R2FR_3083_WEP_COMPONENT_BOUND_ROWS_NONCLAIM.csv",
    "SRC3084_06_1838_doc": ROOT / "1838-Y5-R2FR-ordinary-matter-action-signature-source-label-forgetting-or-WEP-bound-first-fill.md",
    "SRC3084_07_1838_signature": RESIDUALS / "P8_Y5_PARENT_QLOC_1838_ORDINARY_MATTER_SIGNATURE_AUDIT.csv",
    "SRC3084_08_1838_source_label": RESIDUALS / "P8_Y5_PARENT_QLOC_1838_SOURCE_LABEL_FORGETTING_GATE.csv",
    "SRC3084_09_1838_first_wep": RESIDUALS / "P8_Y5_PARENT_QLOC_1838_FIRST_WEP_COMPONENT_BOUND_INPUT.csv",
    "SRC3084_10_1088_MOMS": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
    "SRC3084_11_1090_axioms": ROOT / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md",
    "SRC3084_12_1476_source_label": ROOT / "1476-Y5-R10-RAB-source-label-forgetting-proof-or-Ci-source-weight-numeric-row.md",
    "SRC3084_13_1479_no_prefactor": ROOT / "1479-Y5-R10-RAB-no-source-only-action-prefactor-typing-theorem-or-delta-w-bound-pack.md",
    "SRC3084_14_1766_exchange_graph": ROOT / "1766-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md",
    "SRC3084_15_1686_label_quotient": MICROSCOPE / "branch_locked_wep" / "residuals" / "R2FR_parent_label_quotient_clause_audit_1686.csv",
    "SRC3084_16_1630_AX1090": RESIDUALS / "P8_Y5_PARENT_QLOC_1630_AX1090_REDUCTION_STATUS.csv",
    "SRC3084_17_delta_w_row": MICROSCOPE / "quarantine" / "1476" / "DELTA_W_SOURCE_WEIGHT_INPUT_ROW_NONCLAIM.csv",
    "SRC3084_18_tau_WEP_schema": RESIDUALS / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv",
    "SRC3084_19_MICROSCOPE_provenance": RESIDUALS / "P8_Y5_R10_1069_MICROSCOPE_PROVENANCE_LEDGER.csv",
    "SRC3084_20_branch_lock": MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv",
    "SRC3084_21_eta_convention": MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv",
    "SRC3084_22_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3084_SOURCE_REGISTER.csv",
    "signature_audit": RESIDUALS / "P8_Y5_R2FR_3084_ORDINARY_MATTER_SIGNATURE_AUDIT.csv",
    "source_label_gate": RESIDUALS / "P8_Y5_R2FR_3084_SOURCE_LABEL_FORGETTING_GATE.csv",
    "first_wep_input": RESIDUALS / "P8_Y5_R2FR_3084_FIRST_WEP_COMPONENT_BOUND_INPUT_NONCLAIM.csv",
    "shadow_escape": RESIDUALS / "P8_Y5_R2FR_3084_SOURCE_SHADOW_ESCAPE_LEDGER.csv",
    "corpus_gate": RESIDUALS / "P8_Y5_R2FR_3084_CURRENT_CORPUS_GATE.csv",
    "score_blockers": RESIDUALS / "P8_Y5_R2FR_3084_SCORE_BLOCKER_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3084_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3084_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3084_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3084_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3084_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "signature_copy": LOCAL_BOUNDS / "ordinary_matter_signature_audit_3084_NONCLAIM.csv",
    "source_label_copy": LOCAL_BOUNDS / "source_label_forgetting_gate_3084_NONCLAIM.csv",
    "first_wep_copy": LOCAL_BOUNDS / "WEP_first_component_bound_input_3084_NONCLAIM.csv",
    "shadow_escape_copy": LOCAL_BOUNDS / "source_shadow_escape_ledger_3084_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3084_source_shadow_ban_or_tauWEP_direct_product_NEXT_NONCLAIM.csv",
}

for output_path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    output_path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def row_count(path: Path) -> int:
    if not path.exists():
        return 0
    if path.suffix.lower() == ".csv":
        return len(rows(path))
    return len(path.read_text(encoding="utf-8").splitlines())


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: output_row.get(key, "") for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, Any]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "parent_signed",
        "passes_current_corpus",
        "passes_required_gate",
        "gate_pass",
        "score_allowed",
        "component_claim",
        "operator_ready",
    }
    for input_row in input_rows:
        for field in claim_fields:
            if field in input_row and boolish(input_row[field]):
                return True
    return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for table_row in table_rows:
        lines.append("| " + " | ".join(md_escape(table_row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def copy_csv(source_path: Path, destination_path: Path) -> None:
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, destination_path)


remove_pycache()
dotg_hash_before = file_hash(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "source_path": str(source_path),
            "exists": str(source_path.exists()),
            "parse_ok": str(source_parse_ok(source_path)),
            "row_count": row_count(source_path),
            "role": "ordinary_matter_signature_source_label_evidence"
            if source_id != "SRC3084_22_dotg_target"
            else "append_guard_target",
            "status": "PRESENT" if source_path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, source_path in SOURCE_PATHS.items()
]

signature_rows = [
    base(
        {
            "clause_id": "OMS3084_0_action_form",
            "required_statement": "S_ord = sum_A S_A[Psi_A; E(q(Phi)), Omega(E(q(Phi))), A_obs(q(Phi)), theta_A] with no hidden representative/source-only argument.",
            "if_signed": "ordinary matter sees only quotient-owned observed geometry/gauge data and fixed representation constants",
            "current_status": "EXACT_CONTRACT_NOT_PARENT_DERIVED",
            "blocks": "P_WEP zero theorem;qbar_source_weight zero;local WEP promotion",
            "parent_signed": "false",
            "source_ids": "SRC3084_10_1088_MOMS;SRC3084_11_1090_axioms",
        }
    ),
    base(
        {
            "clause_id": "OMS3084_1_parent_object",
            "required_statement": "one parent action object owns ordinary matter before all readout/projection/fitting choices",
            "if_signed": "prevents stitching separate contracts into a fake derivation",
            "current_status": "PARENT_OBJECT_NOT_PROVEN",
            "blocks": "MOMS adoption as theorem",
            "parent_signed": "false",
            "source_ids": "SRC3084_11_1090_axioms;SRC3084_16_1630_AX1090",
        }
    ),
    base(
        {
            "clause_id": "OMS3084_2_matter_bundle",
            "required_statement": "ordinary matter fields are sections over the observed quotient bundle, with vertical lifts only gauge/boundary/local-Lorentz/diffeomorphism",
            "if_signed": "no physical ordinary-matter lift along quotient-vertical directions",
            "current_status": "MISSING_PARENT_MATTER_BUNDLE_FUNCTOR",
            "blocks": "matter descent",
            "parent_signed": "false",
            "source_ids": "SRC3084_04_3083_dependency;SRC3084_10_1088_MOMS",
        }
    ),
    base(
        {
            "clause_id": "OMS3084_3_constant_superselection",
            "required_statement": "masses, charges, alpha_EM, clock standards, representation labels and hbar/c are q-owned fixed data or retained residual fields",
            "if_signed": "removes hidden material/constant WEP currents",
            "current_status": "CONSTANT_SECTOR_UNSIGNED",
            "blocks": "composition source-current zero;clock and EM marker rows",
            "parent_signed": "false",
            "source_ids": "SRC3084_03_3083_gate;SRC3084_04_3083_dependency",
        }
    ),
    base(
        {
            "clause_id": "OMS3084_4_no_species_weights",
            "required_statement": "no independent w_A(X)S_A, kappa_A T_A, source-only material multiplier, or species-label scalar is an allowed parent argument",
            "if_signed": "Delta_w_TiPt is syntactically impossible before variation",
            "current_status": "SOURCE_ONLY_WEIGHT_EXCLUSION_UNSIGNED",
            "blocks": "WEP material/source row",
            "parent_signed": "false",
            "source_ids": "SRC3084_12_1476_source_label;SRC3084_13_1479_no_prefactor",
        }
    ),
    base(
        {
            "clause_id": "OMS3084_5_variation_order",
            "required_statement": "Hilbert/current extraction occurs before material projection, empirical readout, source-worldtube selection, or calibration",
            "if_signed": "post-variation source selectors cannot manufacture a WEP residual",
            "current_status": "CONDITIONAL_SUBTHEOREM_ONLY",
            "blocks": "readout no-reentry",
            "parent_signed": "false",
            "source_ids": "SRC3084_12_1476_source_label;SRC3084_21_eta_convention",
        }
    ),
    base(
        {
            "clause_id": "OMS3084_6_no_shadow_domain",
            "required_statement": "no shadow source map, matter frame, domain marker, boundary charge, or support/readout marker reintroduces species labels",
            "if_signed": "source-shadow route is eliminated",
            "current_status": "SOURCE_SHADOW_BAN_UNSIGNED",
            "blocks": "local WEP/Newton/PPN transfer",
            "parent_signed": "false",
            "source_ids": "SRC3084_14_1766_exchange_graph;SRC3084_15_1686_label_quotient",
        }
    ),
    base(
        {
            "clause_id": "OMS3084_7_verdict",
            "required_statement": "OMS3084_0 through OMS3084_6 are all parent-signed in one action",
            "if_signed": "P_WEP material/source branch is theorem-zero",
            "current_status": "ORDINARY_MATTER_SIGNATURE_NOT_PARENT_SIGNED",
            "blocks": "P_WEP=0 and local-GR promotion",
            "parent_signed": "false",
            "source_ids": "SRC3084_07_1838_signature;SRC3084_03_3083_gate",
        }
    ),
]

source_label_rows = [
    base(
        {
            "gate_id": "SLG3084_0_total_Hilbert_source",
            "claim_piece": "source functor domain is total Hilbert stress/current",
            "formal_statement": "q_src({(T_A,A)}) = sum_A T_A before gravitational source selection",
            "current_result": "EXACT_CONDITIONAL_THEOREM",
            "countermodel": "F((T_A,A)) = sum_A kappa_A T_A remains covariant/additive if labels survive",
            "passes_current_corpus": "false",
        }
    ),
    base(
        {
            "gate_id": "SLG3084_1_connected_exchange_graph",
            "claim_piece": "ordinary matter exchange graph collapses weights",
            "formal_statement": "if G_ord is connected and weights are natural on exchange morphisms, all w_A=w_*",
            "current_result": "DERIVED_CONDITIONAL_THEOREM_SOURCE_CERT_MISSING",
            "countermodel": "disconnected source-relevant components can carry independent weights",
            "passes_current_corpus": "false",
        }
    ),
    base(
        {
            "gate_id": "SLG3084_2_common_measure_current",
            "claim_piece": "one action measure/current owner",
            "formal_statement": "S_ord/hbar_parent has one action scale, species-blind measure/Jacobian, and one Hilbert/coframe current owner",
            "current_result": "MISSING_AXIOM_NOT_REDUCED",
            "countermodel": "w_A S_A or species-dependent Jacobian changes Hilbert source while preserving isolated EOM form",
            "passes_current_corpus": "false",
        }
    ),
    base(
        {
            "gate_id": "SLG3084_3_no_hidden_hom",
            "claim_piece": "no hidden-visible coefficient map",
            "formal_statement": "Hom(hidden/representative/marker, active-source-prefactor) is absent except through q-owned fixed data",
            "current_result": "NO_HOM_CONTRACT_NOT_PARENT_DERIVED",
            "countermodel": "hidden invariant, marker, readout or current map supplies a finite source prefactor",
            "passes_current_corpus": "false",
        }
    ),
    base(
        {
            "gate_id": "SLG3084_4_readout_no_reentry",
            "claim_piece": "readout/source-worldtube maps preserve label forgetting",
            "formal_statement": "K_readout o q_src has no species-label argument except through the already-summed T_total",
            "current_result": "READOUT_TRANSFER_UNSIGNED",
            "countermodel": "source-worldtube/readout kernel recreates effective source labels after variation",
            "passes_current_corpus": "false",
        }
    ),
    base(
        {
            "gate_id": "SLG3084_5_verdict",
            "claim_piece": "source-label forgetting signs Delta_w_TiPt=0",
            "formal_statement": "SLG3084_0 through SLG3084_4 all parent-signed",
            "current_result": "SOURCE_LABEL_FORGETTING_NOT_DERIVED",
            "countermodel": "relative source-weight/source-shadow countermodels remain legal",
            "passes_current_corpus": "false",
        }
    ),
]

first_wep_rows = [
    base(
        {
            "input_id": "FWCB3084_0_delta_w_TiPt",
            "quantity": "Delta_w_TiPt",
            "definition": "relative ordinary-matter source/action weight for Ti/Pt after removing any common calibration",
            "formula": "q_source^nu = P_loc nabla_mu[Delta_w_TiPt T_TiPt^{mu nu}] + boundary/projector/readout terms",
            "accepted_evidence": "parent theorem-zero certificate OR numeric/source-backed Delta_w_TiPt with units, sign convention, source anchor and no-cancellation statement",
            "current_value": "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W",
            "units": "dimensionless source/action weight",
            "bound_or_gate": "if tau_WEP numeric and nonzero, abs(Delta_w_TiPt) <= eta_bound/abs(tau_WEP); otherwise use direct product evaluator",
            "source_artifact": str(SOURCE_PATHS["SRC3084_17_delta_w_row"]),
            "passes_required_gate": "false",
        }
    ),
    base(
        {
            "input_id": "FWCB3084_1_tau_WEP",
            "quantity": "tau_WEP",
            "definition": "normalized local source/orbit/readout projection converting Delta_w_TiPt into a WEP eta residual",
            "formula": "eta_material_TiPt = Delta_w_TiPt * tau_WEP",
            "accepted_evidence": "parent theorem-zero WEP projection OR numeric local source/orbit/readout integral",
            "current_value": "MISSING_TAU_WEP",
            "units": "dimensionless projection factor",
            "bound_or_gate": "required before converting eta bound into Delta_w width",
            "source_artifact": str(SOURCE_PATHS["SRC3084_18_tau_WEP_schema"]),
            "passes_required_gate": "false",
        }
    ),
    base(
        {
            "input_id": "FWCB3084_2_direct_product",
            "quantity": "P_WEP_material_direct",
            "definition": "unsplit parent product from material/source-weight branch to eta_TiPt",
            "formula": "eta_material_TiPt = P_WEP_material · DeltaGamma_material",
            "accepted_evidence": "derived parent product or sourced numeric product with same branch lock",
            "current_value": "MISSING_DIRECT_PRODUCT",
            "units": "dimensionless eta contribution",
            "bound_or_gate": "alternative to splitting Delta_w_TiPt and tau_WEP",
            "source_artifact": str(SOURCE_PATHS["SRC3084_05_3083_wep_bounds"]),
            "passes_required_gate": "false",
        }
    ),
    base(
        {
            "input_id": "FWCB3084_3_width_rule",
            "quantity": "Delta_w_TiPt_width",
            "definition": "nonclaim prior-width rule if tau_WEP becomes numeric and nonzero",
            "formula": "abs(Delta_w_TiPt)_max = eta_bound / abs(tau_WEP)",
            "accepted_evidence": "tau_WEP numeric plus WEP bound convention and no measured-G absorption",
            "current_value": "NOT_EVALUATED_TAU_WEP_MISSING",
            "units": "dimensionless",
            "bound_or_gate": "width rule only; not a prediction",
            "source_artifact": str(SOURCE_PATHS["SRC3084_19_MICROSCOPE_provenance"]),
            "passes_required_gate": "false",
        }
    ),
    base(
        {
            "input_id": "FWCB3084_4_refusal_guard",
            "quantity": "WEP_material_row_guard",
            "definition": "anti-shortcut rule for the first WEP component row",
            "formula": "reject tau_WEP=1 shortcuts, measured-G absorption, cancellation, surrogate arrays, and branch mixing",
            "accepted_evidence": "branch-locked sourced rows only",
            "current_value": "REFUSAL_ACTIVE",
            "units": "not_applicable",
            "bound_or_gate": "blocks false positives",
            "source_artifact": str(SOURCE_PATHS["SRC3084_20_branch_lock"]),
            "passes_required_gate": "false",
        }
    ),
]

shadow_escape_rows = [
    base(
        {
            "escape_id": "SSE3084_0_shadow_source_map",
            "escape_route": "source map has access to species labels after Hilbert summation",
            "why_it_matters": "recreates Delta_w_TiPt even if isolated matter equations are universal",
            "closure_needed": "prove q_src depends only on T_total and quotient-owned fields",
            "current_status": "SOURCE_SHADOW_BAN_UNSIGNED",
        }
    ),
    base(
        {
            "escape_id": "SSE3084_1_readout_projector",
            "escape_route": "readout/worldtube projector reintroduces material labels",
            "why_it_matters": "moves WEP violation from action to measurement/projection layer",
            "closure_needed": "prove K_readout preserves source-label forgetting or bound the projector",
            "current_status": "READOUT_TRANSFER_UNSIGNED",
        }
    ),
    base(
        {
            "escape_id": "SSE3084_2_shadow_frame_marker",
            "escape_route": "hidden conformal/disformal/material marker frame survives",
            "why_it_matters": "WEP can fail through constants/markers even with common observed geometry",
            "closure_needed": "no-shadow-frame/no-marker theorem or numeric marker coefficient bounds",
            "current_status": "NO_SHADOW_MARKER_UNSIGNED",
        }
    ),
    base(
        {
            "escape_id": "SSE3084_3_tau_direct_product",
            "escape_route": "tau_WEP or direct P_WEP_material product is missing",
            "why_it_matters": "even a Delta_w row cannot become an eta prediction without the projection product",
            "closure_needed": "derive tau_WEP/direct product or source it as nonclaim numeric input",
            "current_status": "TAUWEP_DIRECT_PRODUCT_MISSING",
        }
    ),
]

corpus_gate_rows = [
    base(
        {
            "gate_id": "CG3084_0_MOMS_signature",
            "claim": "ordinary matter action signature is parent-signed",
            "gate_pass": "false",
            "reason": "1088/1090/1630 leave MOMS/AX1090 as exact contract or missing-axiom bundle",
        }
    ),
    base(
        {
            "gate_id": "CG3084_1_source_label_forgetting",
            "claim": "Delta_w_TiPt=0 by source-label forgetting",
            "gate_pass": "false",
            "reason": "1476/1686 keep parent label quotient/source functor unsigned",
        }
    ),
    base(
        {
            "gate_id": "CG3084_2_connected_graph",
            "claim": "ordinary graph connectivity currently proves WEP material-source zero",
            "gate_pass": "false",
            "reason": "1766 conditionally narrows the block but still needs source-backed graph certificate and source-shadow ban",
        }
    ),
    base(
        {
            "gate_id": "CG3084_3_first_component_input",
            "claim": "first WEP material/source component is score-ready",
            "gate_pass": "false",
            "reason": "Delta_w_TiPt, tau_WEP and direct product are still missing",
        }
    ),
    base(
        {
            "gate_id": "CG3084_4_current_WEP",
            "claim": "WEP/local-GR route is promoted",
            "gate_pass": "false",
            "reason": "the route is sharpened but remains nonclaim",
        }
    ),
]

score_blocker_rows = [
    base(
        {
            "blocker_id": "SBL3084_0_signature",
            "blocks": "Delta_w_TiPt theorem-zero",
            "missing": "one parent ordinary-matter action signature with all OMS clauses signed",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3084_1_source_shadow",
            "blocks": "source-label forgetting transfer to local WEP",
            "missing": "source-shadow/readout label re-entry ban",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3084_2_tau_product",
            "blocks": "first material/source WEP input",
            "missing": "tau_WEP or direct P_WEP_material product",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3084_3_no_cancellation",
            "blocks": "WEP component-vector pass",
            "missing": "component-by-component bound or parent cancellation identity",
            "status": "GUARD_ACTIVE",
            "score_allowed": "false",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3084_0_signature_attempt",
            "decision": "ORDINARY_MATTER_SIGNATURE_NOT_PARENT_SIGNED",
            "reason": "MOMS/AX1090 clauses are exact but remain missing parent axioms, not current derivations",
            "next_action": "do not set Delta_w_TiPt=0",
        }
    ),
    base(
        {
            "decision_id": "DEC3084_1_first_bound_row",
            "decision": "FIRST_WEP_MATERIAL_SOURCE_BOUND_INPUT_FILLED_NONCLAIM",
            "reason": "Delta_w_TiPt and tau_WEP/direct product are now explicit row requirements with refusal guards",
            "next_action": "either prove source-shadow ban or source tau_WEP/direct product",
        }
    ),
    base(
        {
            "decision_id": "DEC3084_2_best_next",
            "decision": "SOURCE_SHADOW_BAN_OR_TAUWEP_DIRECT_PRODUCT_NEXT",
            "reason": "after connected ordinary matter, the cleanest escape hatch is a shadow source map or readout projector that recreates labels",
            "next_action": "3085-Y5-R2FR-source-shadow-ban-or-tauWEP-direct-product-first-source-row-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3084_0_signature",
            "claim": "ordinary matter action signature is current MTS theorem",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "signature is an exact contract but not parent-derived",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3084_1_delta_w_zero",
            "claim": "Delta_w_TiPt=0",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "source-label forgetting and shadow-source transfer remain unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3084_2_wep_bound_input",
            "claim": "first WEP material/source row is score-ready",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "Delta_w_TiPt, tau_WEP and direct product are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3084_3_local_GR",
            "claim": "local GR/Newton recovery follows",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "WEP material/source branch is only one unresolved local coupling channel",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3084_0_3085",
            "next_checkpoint": "3085-Y5-R2FR-source-shadow-ban-or-tauWEP-direct-product-first-source-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_source_shadow_ban_or_tauWEP_direct_product_first_source_row_under_AX1090_3085.py",
            "mission": "try to prove the source map is only the total Hilbert source with no shadow/readout label re-entry; if it fails, fill tau_WEP/direct-product first source row as nonclaim",
            "starting_equation": "eta_material_TiPt = Delta_w_TiPt*tau_WEP or eta_material_TiPt = P_WEP_material·DeltaGamma_material",
            "claim_policy": "no WEP/local-GR claim until source-shadow ban is parent-signed or tau_WEP/direct-product rows are sourced, branch-locked and componentwise bounded",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["signature_audit"], signature_rows)
write_csv(OUTPUTS["source_label_gate"], source_label_rows)
write_csv(OUTPUTS["first_wep_input"], first_wep_rows)
write_csv(OUTPUTS["shadow_escape"], shadow_escape_rows)
write_csv(OUTPUTS["corpus_gate"], corpus_gate_rows)
write_csv(OUTPUTS["score_blockers"], score_blocker_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["signature_audit"], BRANCH_OUTPUTS["signature_copy"])
copy_csv(OUTPUTS["source_label_gate"], BRANCH_OUTPUTS["source_label_copy"])
copy_csv(OUTPUTS["first_wep_input"], BRANCH_OUTPUTS["first_wep_copy"])
copy_csv(OUTPUTS["shadow_escape"], BRANCH_OUTPUTS["shadow_escape_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(source_path),
            "copy_path": str(copy_path),
            "copy_exists": str(copy_path.exists()),
            "copy_parse_ok": str(csv_ok(copy_path)),
            "status": "BRANCH_COPY_READY_NONCLAIM" if copy_path.exists() else "BRANCH_COPY_MISSING",
        }
    )
    for copy_id, source_path, copy_path in [
        ("BR3084_0_signature", OUTPUTS["signature_audit"], BRANCH_OUTPUTS["signature_copy"]),
        ("BR3084_1_source_label", OUTPUTS["source_label_gate"], BRANCH_OUTPUTS["source_label_copy"]),
        ("BR3084_2_first_wep", OUTPUTS["first_wep_input"], BRANCH_OUTPUTS["first_wep_copy"]),
        ("BR3084_3_shadow_escape", OUTPUTS["shadow_escape"], BRANCH_OUTPUTS["shadow_escape_copy"]),
        ("BR3084_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)

DOC.write_text("# 3084 - Ordinary Matter Action Signature\n\nPreparing validation.\n", encoding="utf-8")

dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
generated_rows = (
    source_register
    + signature_rows
    + source_label_rows
    + first_wep_rows
    + shadow_escape_rows
    + corpus_gate_rows
    + score_blocker_rows
    + decision_rows
    + claim_rows
    + next_rows
    + branch_rows
)
formalization_output_count = sum(1 for output_path in generated_csvs + [DOC] if under(output_path, FORMALIZATION))
required_signature_ids = {
    "OMS3084_0_action_form",
    "OMS3084_1_parent_object",
    "OMS3084_2_matter_bundle",
    "OMS3084_3_constant_superselection",
    "OMS3084_4_no_species_weights",
    "OMS3084_5_variation_order",
    "OMS3084_6_no_shadow_domain",
    "OMS3084_7_verdict",
}
required_source_label_ids = {
    "SLG3084_0_total_Hilbert_source",
    "SLG3084_1_connected_exchange_graph",
    "SLG3084_2_common_measure_current",
    "SLG3084_3_no_hidden_hom",
    "SLG3084_4_readout_no_reentry",
    "SLG3084_5_verdict",
}
required_first_wep_ids = {
    "FWCB3084_0_delta_w_TiPt",
    "FWCB3084_1_tau_WEP",
    "FWCB3084_2_direct_product",
    "FWCB3084_3_width_rule",
    "FWCB3084_4_refusal_guard",
}
required_shadow_ids = {
    "SSE3084_0_shadow_source_map",
    "SSE3084_1_readout_projector",
    "SSE3084_2_shadow_frame_marker",
    "SSE3084_3_tau_direct_product",
}
signature_verdict = next(row for row in signature_rows if row["clause_id"] == "OMS3084_7_verdict")
source_label_verdict = next(row for row in source_label_rows if row["gate_id"] == "SLG3084_5_verdict")
current_wep_gate = next(row for row in corpus_gate_rows if row["gate_id"] == "CG3084_4_current_WEP")

validation_rows = [
    base(
        {
            "validation_id": "VAL3084_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3084_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3084_02_csv_parse",
            "passed": str(all(csv_ok(output_path) for output_path in generated_csvs if output_path != OUTPUTS["validation"])),
            "requirement": "all generated and branch-copy CSVs parse cleanly before validation write",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3084_03_signature_rows_complete",
            "passed": str(required_signature_ids.issubset({row["clause_id"] for row in signature_rows}) and not has_claim_true(signature_rows)),
            "requirement": "ordinary matter signature audit covers action form, parent object, matter bundle, constants, species weights, variation order, shadow domain and verdict as nonclaim rows",
            "evidence": OUTPUTS["signature_audit"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3084_04_signature_verdict_refuses_claim",
            "passed": str(signature_verdict["current_status"] == "ORDINARY_MATTER_SIGNATURE_NOT_PARENT_SIGNED" and signature_verdict["parent_signed"] == "false"),
            "requirement": "ordinary matter signature is not parent-signed",
            "evidence": OUTPUTS["signature_audit"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3084_05_source_label_gate_complete",
            "passed": str(required_source_label_ids.issubset({row["gate_id"] for row in source_label_rows}) and not has_claim_true(source_label_rows)),
            "requirement": "source-label forgetting gate records all required subclauses and refuses current corpus claim",
            "evidence": OUTPUTS["source_label_gate"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3084_06_source_label_verdict_refuses_delta_w_zero",
            "passed": str(source_label_verdict["current_result"] == "SOURCE_LABEL_FORGETTING_NOT_DERIVED" and source_label_verdict["passes_current_corpus"] == "false"),
            "requirement": "Delta_w_TiPt=0 is not promoted",
            "evidence": OUTPUTS["source_label_gate"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3084_07_first_wep_inputs_present_nonclaim",
            "passed": str(required_first_wep_ids.issubset({row["input_id"] for row in first_wep_rows}) and not has_claim_true(first_wep_rows)),
            "requirement": "Delta_w, tau_WEP, direct product, width rule and refusal guard are present as nonclaim WEP inputs",
            "evidence": OUTPUTS["first_wep_input"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3084_08_shadow_escape_ledger_present",
            "passed": str(required_shadow_ids.issubset({row["escape_id"] for row in shadow_escape_rows}) and not has_claim_true(shadow_escape_rows)),
            "requirement": "shadow source, readout projector, shadow marker and tau/direct-product escape routes are recorded",
            "evidence": OUTPUTS["shadow_escape"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3084_09_current_gate_blocks_wep",
            "passed": str(current_wep_gate["gate_pass"] == "false" and not has_claim_true(corpus_gate_rows)),
            "requirement": "current corpus gate blocks WEP/local-GR promotion",
            "evidence": OUTPUTS["corpus_gate"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3084_10_score_blockers_active",
            "passed": str(not has_claim_true(score_blocker_rows) and all(row["status"] in {"BLOCKS_SCORE", "GUARD_ACTIVE"} for row in score_blocker_rows)),
            "requirement": "signature, source-shadow, tau/direct-product and no-cancellation blockers remain active",
            "evidence": OUTPUTS["score_blockers"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3084_11_no_claim_promoted",
            "passed": str(not has_claim_true(generated_rows)),
            "requirement": "no ordinary matter signature, Delta_w zero, WEP, local-GR or Newton claim is promoted",
            "evidence": "claim field scan",
        }
    ),
    base(
        {
            "validation_id": "VAL3084_12_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3085-Y5-R2FR-source-shadow-ban-or-tauWEP")),
            "requirement": "next target moves to source-shadow ban or tau_WEP/direct product",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3084_13_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3084_14_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3084_15_outputs_under_post_checkpoint",
            "passed": str(all(under(output_path, ROOT) for output_path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3084_16_no_formalization_outputs",
            "passed": str(formalization_output_count == 0),
            "requirement": "formalization-workbench modified-file count for 3084 outputs remains zero",
            "evidence": f"formalization_3084_output_paths={formalization_output_count}",
        }
    ),
    base(
        {
            "validation_id": "VAL3084_17_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3084_18_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
]

write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3084 - Ordinary Matter Action Signature, Source-Label Forgetting, or First WEP Bound Fill

Status: `Y5_R2FR_3084_ordinary_matter_signature_refused_first_WEP_input_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3084 tries the clean theorem route first. If a single parent ordinary-matter action owns the observed geometry, constants, measure/current, variation-before-readout order and source-label forgetting, then the WEP material/source branch is theorem-zero.

The theorem shape is strong, but the current corpus still does **not** sign the full ordinary-matter action signature. In particular, source-label forgetting can still be defeated by a shadow source/readout map that reintroduces labels after variation.

So the checkpoint refuses `Delta_w_TiPt=0`, refuses a WEP score, and fills the first WEP component-bound input rows as nonclaim: `Delta_w_TiPt`, `tau_WEP`, the direct material product, the width rule, and the refusal guard.

The next best target is therefore source-shadow closure or the first real `tau_WEP`/direct-product source row. This is not circling; this is tightening the coupling noose.

## Ordinary Matter Signature Audit

{md_table(signature_rows, ["clause_id", "required_statement", "current_status", "blocks", "parent_signed"])}

## Source-Label Forgetting Gate

{md_table(source_label_rows, ["gate_id", "claim_piece", "current_result", "countermodel", "passes_current_corpus"])}

## First WEP Component Bound Input

{md_table(first_wep_rows, ["input_id", "quantity", "formula", "current_value", "passes_required_gate"])}

## Source-Shadow Escape Ledger

{md_table(shadow_escape_rows, ["escape_id", "escape_route", "why_it_matters", "closure_needed", "current_status"])}

## Current Corpus Gate

{md_table(corpus_gate_rows, ["gate_id", "claim", "gate_pass", "reason"])}

## Score Blockers

{md_table(score_blocker_rows, ["blocker_id", "blocks", "missing", "status"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "reason", "next_action"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "claim_active", "status", "reason"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files

- Source register: `{OUTPUTS["sources"]}`
- Ordinary matter signature audit: `{OUTPUTS["signature_audit"]}`
- Source-label forgetting gate: `{OUTPUTS["source_label_gate"]}`
- First WEP component input: `{OUTPUTS["first_wep_input"]}`
- Source-shadow escape ledger: `{OUTPUTS["shadow_escape"]}`
- Current corpus gate: `{OUTPUTS["corpus_gate"]}`
- Score blockers: `{OUTPUTS["score_blockers"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
- Branch copy: `{BRANCH_OUTPUTS["signature_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["source_label_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["first_wep_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["shadow_escape_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["next_copy"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
remove_pycache()

print(f"Wrote {DOC}")
print(f"Wrote {OUTPUTS['validation']}")
print(f"Validation passed {sum(1 for row in validation_rows if row['passed'] == 'True')}/{len(validation_rows)}")
