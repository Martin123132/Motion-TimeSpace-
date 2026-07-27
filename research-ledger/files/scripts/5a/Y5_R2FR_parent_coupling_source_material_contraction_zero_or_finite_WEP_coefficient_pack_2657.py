from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2657"
BRANCH_LOCK = ROOT / "source-intake" / "microscope" / "branch_locked_wep"
CMSM_DROP = ROOT / "source-intake" / "microscope_cmsm"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2657-Y5-R2FR-parent-coupling-source-material-contraction-zero-or-finite-WEP-coefficient-pack.md"

CHECKPOINT = "2657"
BRANCH_ID = "Y5_R2FR_PARENT_COUPLING_SOURCE_MATERIAL_CONTRACTION_2657"
PARENT_BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
PREFIX = "P8_Y5_PARENT_CONTRACTION_2657"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "live_import_audit": RESIDUALS / f"{PREFIX}_LIVE_IMPORT_AUDIT.csv",
    "contraction_zero_attempt": RESIDUALS / f"{PREFIX}_CONTRACTION_ZERO_THEOREM_ATTEMPT.csv",
    "finite_coefficient_pack": RESIDUALS / f"{PREFIX}_FINITE_WEP_COEFFICIENT_PACK_NONCLAIM.csv",
    "coefficient_pack_gate": RESIDUALS / f"{PREFIX}_COEFFICIENT_PACK_EXECUTABILITY_GATE.csv",
    "dryrun_cases": RESIDUALS / f"{PREFIX}_CONTRACTION_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / f"{PREFIX}_CONTRACTION_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2657_FINITE_WEP_COEFFICIENT_PACK_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "WEP_parent_contraction_2657_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "WEP_PARENT_CONTRACTION_2657_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2657_CONTRACTION_ZERO_THEOREM_ATTEMPT.csv",
    "quarantine": QUARANTINE / "P8_Y5_2657_CONTRACTION_DRYRUN_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2656_doc": {
        "path": ROOT / "2656-Y5-R2FR-official-MICROSCOPE-readout-data-dry-run-or-source-worldtube-residual-bound.md",
        "needles": ["BIC2656_1_C_parent", "SRB2656_5_verdict", "NEXT2656_0_selected", "VAL2656_OVERALL"],
        "role": "immediate handoff selecting parent coupling/source/material contraction",
    },
    "1484_doc": {
        "path": ROOT / "1484-Y5-R10-RAB-branch-locked-WEP-product-interface-or-C-parent-coupling-derivation.md",
        "needles": ["WPI1484_1_C_parent", "CPD1484_5_verdict", "VAL1484_17_overall"],
        "role": "branch-locked product interface and C_parent derivation gap",
    },
    "1485_doc": {
        "path": ROOT / "1485-Y5-R10-RAB-C-parent-WEP-functional-derivative-or-universal-matter-double-zero-proof.md",
        "needles": ["DZ1485_5_verdict", "IMP1485_2_derived_zero", "VAL1485_18_overall"],
        "role": "functional derivative and exact conditional double-zero theorem",
    },
    "1426_doc": {
        "path": ROOT / "1426-Y5-R10-RAB-active-source-prefactor-admissibility-or-finite-WEP-coefficient-pack.md",
        "needles": ["ADM1426_5_verdict", "PACK1426_0_C_parent", "VAL1426_9_overall"],
        "role": "active-source prefactor countermodel and finite coefficient pack",
    },
    "1430_doc": {
        "path": ROOT / "1430-Y5-R10-RAB-C-parent-coupling-source-signature-or-refusal-ledger.md",
        "needles": ["CP1430_6_verdict", "CPC1430_3_claim_rule", "VAL1430_8_overall"],
        "role": "branch-locked C_parent placeholder/refusal ledger",
    },
    "1438_doc": {
        "path": ROOT / "1438-Y5-R10-RAB-WEP-slot-C-parent-zero-or-official-source-pack-intake.md",
        "needles": ["CZ1438_5_zero_certificate", "CPS1438_0_WEP_C_parent", "VAL1438_12_overall"],
        "role": "C_parent WEP slot zero/import lock",
    },
    "1450_doc": {
        "path": ROOT / "1450-Y5-R10-RAB-source-label-forgetting-Hilbert-current-theorem-or-relative-weight-bound-ledger.md",
        "needles": ["HT1450_6_verdict", "EVAL1450_0_source_label", "VAL1450_8_not_evaluable"],
        "role": "Hilbert source-label theorem and active source prefactor blocker",
    },
    "2654_doc": {
        "path": ROOT / "2654-Y5-R2FR-WEP-source-worldtube-material-tensor-acquisition-or-action-owner-lemma.md",
        "needles": ["ACO2654_6_verdict", "AOG2654_4_verdict", "VAL2654_OVERALL"],
        "role": "action/current owner gap for WEP source residuals",
    },
}

LIVE_IMPORT_TARGETS: dict[str, dict[str, Any]] = {
    "C_parent_placeholder": {
        "path": BRANCH_LOCK / "coefficients" / "C_parent.csv",
        "required_status": "placeholder/refusal only, not a live coefficient",
        "role": "existing branch-locked C_parent refusal file",
    },
    "C_parent_WEP_slot_import": {
        "path": BRANCH_LOCK / "coefficients" / "C_parent_WEP_slot_import.csv",
        "required_status": "DERIVED_ZERO or source-backed finite coefficient with units/sign/basis",
        "role": "live coefficient import target",
    },
    "C_parent_import_schema": {
        "path": BRANCH_LOCK / "coefficients" / "C_parent_import_schema.csv",
        "required_status": "schema only",
        "role": "coefficient import schema",
    },
    "full_material_tensor": {
        "path": ROOT / "source-intake" / "microscope" / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv",
        "required_status": "source-backed full material tensor in parent basis",
        "role": "material response tensor target",
    },
    "official_cmsm_drop": {
        "path": CMSM_DROP,
        "required_status": "official arrays/schema/manifest, not helper templates",
        "role": "readout kernel side gate",
    },
    "branch_id": {
        "path": BRANCH_LOCK / "branch_id.csv",
        "required_status": f"must declare {PARENT_BRANCH}",
        "role": "same-parent branch guard",
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2657_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def has_placeholder_tokens(path: Path) -> bool:
    text = read_text(path)
    tokens = ("MISSING", "PENDING", "PLACEHOLDER", "NOT_SCOREABLE", "REFUSED", "NOT_CLAIM")
    return any(token in text for token in tokens)


def directory_candidate_count(path: Path) -> int:
    if not path.exists() or not path.is_dir():
        return 0
    helper_prefixes = ("README", "TEMPLATE")
    count = 0
    for item in path.rglob("*"):
        if item.is_file() and not item.name.upper().startswith(helper_prefixes):
            count += 1
    return count


def live_import_audit_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for target_id, spec in LIVE_IMPORT_TARGETS.items():
        path = Path(spec["path"])
        exists = path.exists()
        parseable_csv = False
        placeholder_tokens = False
        candidate_count = ""
        if exists and path.is_file() and path.suffix.lower() == ".csv":
            try:
                parseable_csv = len(csv_rows(path)) >= 1
                placeholder_tokens = has_placeholder_tokens(path)
            except Exception:
                parseable_csv = False
        if exists and path.is_dir():
            candidate_count = directory_candidate_count(path)
        if target_id == "C_parent_placeholder":
            status = "PLACEHOLDER_FILE_EXISTS_NONCLAIM" if exists and parseable_csv and placeholder_tokens else "PLACEHOLDER_FILE_STATUS_UNEXPECTED"
        elif target_id == "C_parent_import_schema":
            status = "SCHEMA_EXISTS_NOT_COEFFICIENT" if exists and parseable_csv else "SCHEMA_MISSING"
        elif target_id == "official_cmsm_drop":
            status = "NO_OFFICIAL_ARRAY_CANDIDATES" if exists and candidate_count == 0 else "CANDIDATE_FILES_REQUIRE_VALIDATION"
        elif target_id == "branch_id":
            text = read_text(path)
            status = "BRANCH_ID_PRESENT" if exists and PARENT_BRANCH in text else "BRANCH_ID_MISSING_OR_MISMATCH"
        else:
            status = "LIVE_IMPORT_MISSING" if not exists else "PRESENT_REQUIRES_STRICT_VALIDATION"
        rows.append(
            {
                "audit_id": f"LIA2657_{target_id}",
                "role": spec["role"],
                "path": str(path),
                "required_status": spec["required_status"],
                "exists": exists,
                "parseable_csv": parseable_csv,
                "placeholder_tokens": placeholder_tokens,
                "directory_candidate_count": candidate_count,
                "audit_status": status,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def contraction_zero_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "PCZ2657_0_target",
            "claim_piece": "parent coupling/source/material contraction zero",
            "formal_statement": "For WEP/local GR, eta_pred = |sum_X C_parent_X R_material_X tau_eff_X| must vanish by parent theorem or remain a finite coefficient product with sourced factors.",
            "status": "TARGET_SHARP",
            "proof_or_gap": "this turns the local GR/Newton route into a product-zero/product-bound problem instead of a plateau axiom",
            "source_anchor": "2656:SRB2656_1_operator_decomposition;1484:WPI1484_0_formula",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PCZ2657_1_functional_derivative_definition",
            "claim_piece": "C_parent_X owner",
            "formal_statement": "C_parent_X := N_X^{-1} dS_parent(Phi + s V_WEP,X)/ds at s=0, with N_X, units, sign and parent response basis declared before comparison.",
            "status": "EXACT_DEFINITION_CONDITIONAL_ON_PARENT_ACTION_AND_GENERATOR",
            "proof_or_gap": "the coefficient has a legal mathematical definition, but the parent action, V_WEP generator, and normalization are not jointly source-signed",
            "source_anchor": "1485:FD1485_5_verdict;1484:CPD1484_1_functional_derivative",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PCZ2657_2_neighbourhood_double_zero",
            "claim_piece": "derived zero route",
            "formal_statement": "If ordinary matter descends through q(Phi) on an open fibre neighbourhood and V_WEP,X is vertical throughout that neighbourhood, then C_parent_X(Phi)=0 and partial_A C_parent_X(Phi0)=0.",
            "status": "EXACT_CONDITIONAL_THEOREM_REUSED",
            "proof_or_gap": "the proof is solid as conditional mathematics; the corpus has not parent-signed neighbourhood descent, MOMS, no w_A, no hidden spurion and readout silence",
            "source_anchor": "1485:DZ1485_0_exact_neighbourhood_theorem;1485:DZ1485_5_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PCZ2657_3_contraction_zero_corollary",
            "claim_piece": "WEP product zero if C_parent is theorem-zero",
            "formal_statement": "If C_parent_X=0 for every active WEP channel before readout, then eta_pred=0 independently of the finite material/source/readout factors, provided readout does not reintroduce hidden labels.",
            "status": "EXACT_CONDITIONAL_COROLLARY",
            "proof_or_gap": "product zero follows immediately from the locked product law, but readout/hidden-label silence remains a theorem premise, not a current result",
            "source_anchor": "1484:WPI1484_0_formula;1438:CZ1438_4_no_readout_leak",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PCZ2657_4_countermodels",
            "claim_piece": "surviving nonzero routes",
            "formal_statement": "Pre-variation w_A weights, hidden marker coefficients, non-Hilbert currents, boundary/projector leakage, or finite source-material response rows can make the contraction nonzero.",
            "status": "COUNTERMODELS_RETAINED",
            "proof_or_gap": "these are not embarrassing add-ons; they are the exact finite residual channels that must be theorem-zero or source-bounded",
            "source_anchor": "1426:CM1426_0_pre_variation_wA;1450:HT1450_5_nonHilbert_guard;2654:ACO2654_6_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PCZ2657_5_verdict",
            "claim_piece": "promote parent contraction zero to local-GR/WEP theorem",
            "formal_statement": "Current MTS parent primitives prove the WEP coupling/source/material contraction vanishes in the local GR/Newton branch.",
            "status": "CONTRACTION_ZERO_THEOREM_NOT_PARENT_DERIVED",
            "proof_or_gap": "the exact conditional route exists, but neighbourhood descent, ordinary-matter signature, no source-only slot, source-current owner, full material tensor and readout silence are not jointly signed",
            "source_anchor": "PCZ2657_0_target through PCZ2657_4_countermodels",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def finite_coefficient_pack_rows() -> list[dict[str, Any]]:
    return [
        {"pack_id": "FWP2657_0_C_parent_zero", "factor": "C_parent_X theorem-zero certificate", "required_form": "parent-signed DERIVED_ZERO from neighbourhood quotient descent and V_WEP verticality", "current_artifact": "MISSING_PARENT_SIGNED_ZERO_CERTIFICATE", "current_status": "ZERO_ROUTE_NOT_CLOSED", "units": "dimensionless or declared parent coefficient units", "source_anchor": "1485:DZ1485_5_verdict", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"pack_id": "FWP2657_1_C_parent_finite", "factor": "C_parent_X finite coefficient", "required_form": "source-backed numeric coefficient with value, uncertainty, units, sign, branch, basis, and parent_status", "current_artifact": str(BRANCH_LOCK / "coefficients" / "C_parent.csv"), "current_status": "PLACEHOLDER_ROWS_ONLY_NOT_IMPORTABLE", "units": "pending parent basis", "source_anchor": "1430:CP1430_6_verdict", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"pack_id": "FWP2657_2_R_material", "factor": "R_material_X(TA6V-PtRh10)", "required_form": "full parent-basis material tensor with double-count rule and source path", "current_artifact": "MISSING_FULL_PARENT_MATERIAL_TENSOR", "current_status": "MISSING_FULL_MATERIAL_TENSOR", "units": "dimensionless sensitivities per parent response channel", "source_anchor": "1424:SRCMAP1424_1_R_material;1438:PACK1438_4_material_tensor", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"pack_id": "FWP2657_3_R_source", "factor": "R_source^Earth", "required_form": "profile/worldtube-weighted source vector in the same parent response basis, or theorem common-mode zero", "current_artifact": "MISSING_SOURCE_PROFILE_WEIGHTING", "current_status": "MISSING_SOURCE_VECTOR", "units": "dimensionless source vector or normalized kernel", "source_anchor": "1424:SRCMAP1424_0_R_source;2656:BIC2656_2_R_source", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"pack_id": "FWP2657_4_K_CMSM_tau", "factor": "K_CMSM/tau_eff_X", "required_form": "official arrays or validated reconstruction plus tau/readout product convention", "current_artifact": str(CMSM_DROP), "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED_TAU_NOT_DERIVED", "units": "dimensionless eta after declared source/readout normalization", "source_anchor": "2656:BIC2656_4_K_CMSM;2656:BIC2656_6_tau_WEP", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"pack_id": "FWP2657_5_measured_G_guard", "factor": "common-mode calibration guard", "required_form": "universal scalar absorbed once; relative/range/frame residuals retained", "current_artifact": "GUARD_DERIVED_NONCLAIM", "current_status": "GUARD_AVAILABLE_BUT_NOT_ZERO_THEOREM", "units": "calibration rule", "source_anchor": "1901:GMG1901_5_verdict", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"pack_id": "FWP2657_6_same_branch_lock", "factor": "single branch/basis/product convention", "required_form": "C_parent, R_material, R_source, K_CMSM/tau and eta convention all share one branch id and no placeholders", "current_artifact": PARENT_BRANCH, "current_status": "BRANCH_ID_EXISTS_BUT_FACTORS_MISSING", "units": "branch/basis metadata", "source_anchor": "1484:WPI1484_5_branch_guard", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"pack_id": "FWP2657_7_acceptance", "factor": "finite WEP coefficient product", "required_form": "derived zero or all finite factors source-backed; absolute no-cancellation envelope below bound", "current_artifact": "NONCLAIM_PACK_ONLY", "current_status": "FINITE_WEP_COEFFICIENT_PACK_NOT_EXECUTABLE", "units": "dimensionless eta envelope", "source_anchor": "FWP2657_0_C_parent_zero through FWP2657_6_same_branch_lock", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
    ]


def coefficient_pack_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CPG2657_0_zero_certificate", "required_clause": "C_parent theorem-zero is parent-signed", "current_status": "FAIL_CONTRACTION_ZERO_THEOREM_NOT_PARENT_DERIVED", "source_anchor": "PCZ2657_5_verdict", "gate_pass": False, "blocks_claim": True, "valid_for_claim": False},
        {"gate_id": "CPG2657_1_finite_Cparent", "required_clause": "finite C_parent coefficient has source-backed value/uncertainty/units/sign", "current_status": "FAIL_PLACEHOLDER_ONLY", "source_anchor": "FWP2657_1_C_parent_finite", "gate_pass": False, "blocks_claim": True, "valid_for_claim": False},
        {"gate_id": "CPG2657_2_material_source", "required_clause": "R_material and R_source are in the same parent basis", "current_status": "FAIL_MISSING_MATERIAL_AND_SOURCE_VECTORS", "source_anchor": "FWP2657_2_R_material;FWP2657_3_R_source", "gate_pass": False, "blocks_claim": True, "valid_for_claim": False},
        {"gate_id": "CPG2657_3_readout_tau", "required_clause": "K_CMSM/tau_eff are official/sourced and not unity shortcuts", "current_status": "FAIL_OFFICIAL_ARRAYS_AND_TAU_MISSING", "source_anchor": "FWP2657_4_K_CMSM_tau", "gate_pass": False, "blocks_claim": True, "valid_for_claim": False},
        {"gate_id": "CPG2657_4_branch_lock", "required_clause": "all factors share one branch/basis and no placeholders", "current_status": "FAIL_FACTORS_MISSING_DESPITE_BRANCH_ID", "source_anchor": "FWP2657_6_same_branch_lock", "gate_pass": False, "blocks_claim": True, "valid_for_claim": False},
        {"gate_id": "CPG2657_5_verdict", "required_clause": "finite WEP coefficient pack is executable", "current_status": "FINITE_WEP_COEFFICIENT_PACK_NOT_EXECUTABLE", "source_anchor": "CPG2657_0_zero_certificate through CPG2657_4_branch_lock", "gate_pass": False, "blocks_claim": True, "valid_for_claim": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY2657_0_unsigned_zero", "zero_parent_signed": False, "closure_only_zero": False, "finite_Cparent": False, "bound_inversion": False, "dd_proxy": False, "source_vector": False, "material_tensor": False, "readout_tau": False, "mixed_basis": False, "tau_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_ZERO_THEOREM_NOT_PARENT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY2657_1_closure_zero", "zero_parent_signed": False, "closure_only_zero": True, "finite_Cparent": False, "bound_inversion": False, "dd_proxy": False, "source_vector": False, "material_tensor": False, "readout_tau": False, "mixed_basis": False, "tau_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_CLOSURE_ONLY_ZERO", "valid_for_claim": False},
        {"case_id": "DRY2657_2_bound_inversion", "zero_parent_signed": False, "closure_only_zero": False, "finite_Cparent": True, "bound_inversion": True, "dd_proxy": False, "source_vector": True, "material_tensor": True, "readout_tau": True, "mixed_basis": False, "tau_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_BOUND_INVERSION_AS_COEFFICIENT", "valid_for_claim": False},
        {"case_id": "DRY2657_3_dd_proxy", "zero_parent_signed": False, "closure_only_zero": False, "finite_Cparent": True, "bound_inversion": False, "dd_proxy": True, "source_vector": True, "material_tensor": True, "readout_tau": True, "mixed_basis": False, "tau_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_DD_PROXY_AS_PARENT_COEFFICIENT", "valid_for_claim": False},
        {"case_id": "DRY2657_4_placeholder_Cparent", "zero_parent_signed": False, "closure_only_zero": False, "finite_Cparent": False, "bound_inversion": False, "dd_proxy": False, "source_vector": True, "material_tensor": True, "readout_tau": True, "mixed_basis": False, "tau_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_C_PARENT_MISSING_OR_PLACEHOLDER", "valid_for_claim": False},
        {"case_id": "DRY2657_5_source", "zero_parent_signed": False, "closure_only_zero": False, "finite_Cparent": True, "bound_inversion": False, "dd_proxy": False, "source_vector": False, "material_tensor": True, "readout_tau": True, "mixed_basis": False, "tau_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_SOURCE_VECTOR_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2657_6_material", "zero_parent_signed": False, "closure_only_zero": False, "finite_Cparent": True, "bound_inversion": False, "dd_proxy": False, "source_vector": True, "material_tensor": False, "readout_tau": True, "mixed_basis": False, "tau_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_MATERIAL_TENSOR_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2657_7_readout_tau", "zero_parent_signed": False, "closure_only_zero": False, "finite_Cparent": True, "bound_inversion": False, "dd_proxy": False, "source_vector": True, "material_tensor": True, "readout_tau": False, "mixed_basis": False, "tau_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_READOUT_TAU_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2657_8_mixed_basis", "zero_parent_signed": False, "closure_only_zero": False, "finite_Cparent": True, "bound_inversion": False, "dd_proxy": False, "source_vector": True, "material_tensor": True, "readout_tau": True, "mixed_basis": True, "tau_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_MIXED_BRANCH_OR_BASIS", "valid_for_claim": False},
        {"case_id": "DRY2657_9_tau_unity", "zero_parent_signed": False, "closure_only_zero": False, "finite_Cparent": True, "bound_inversion": False, "dd_proxy": False, "source_vector": True, "material_tensor": True, "readout_tau": True, "mixed_basis": False, "tau_unity": True, "uses_cancellation": False, "expected_status": "REFUSED_TAU_UNITY_SHORTCUT", "valid_for_claim": False},
        {"case_id": "DRY2657_10_cancellation", "zero_parent_signed": False, "closure_only_zero": False, "finite_Cparent": True, "bound_inversion": False, "dd_proxy": False, "source_vector": True, "material_tensor": True, "readout_tau": True, "mixed_basis": False, "tau_unity": False, "uses_cancellation": True, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False},
        {"case_id": "DRY2657_11_counterfactual_zero", "zero_parent_signed": True, "closure_only_zero": False, "finite_Cparent": False, "bound_inversion": False, "dd_proxy": False, "source_vector": False, "material_tensor": False, "readout_tau": False, "mixed_basis": False, "tau_unity": False, "uses_cancellation": False, "expected_status": "COUNTERFACTUAL_ZERO_READY_NOT_CURRENT_CLAIM", "valid_for_claim": False},
        {"case_id": "DRY2657_12_counterfactual_finite", "zero_parent_signed": False, "closure_only_zero": False, "finite_Cparent": True, "bound_inversion": False, "dd_proxy": False, "source_vector": True, "material_tensor": True, "readout_tau": True, "mixed_basis": False, "tau_unity": False, "uses_cancellation": False, "expected_status": "COUNTERFACTUAL_FINITE_READY_NOT_CURRENT_CLAIM", "valid_for_claim": False},
    ]


def evaluate_dryrun(row: dict[str, Any]) -> str:
    if row["zero_parent_signed"]:
        return "COUNTERFACTUAL_ZERO_READY_NOT_CURRENT_CLAIM"
    if row["closure_only_zero"]:
        return "REFUSED_CLOSURE_ONLY_ZERO"
    if not row["finite_Cparent"]:
        return "REFUSED_ZERO_THEOREM_NOT_PARENT_DERIVED" if not row["source_vector"] else "REFUSED_C_PARENT_MISSING_OR_PLACEHOLDER"
    if row["bound_inversion"]:
        return "REFUSED_BOUND_INVERSION_AS_COEFFICIENT"
    if row["dd_proxy"]:
        return "REFUSED_DD_PROXY_AS_PARENT_COEFFICIENT"
    if not row["source_vector"]:
        return "REFUSED_SOURCE_VECTOR_MISSING"
    if not row["material_tensor"]:
        return "REFUSED_MATERIAL_TENSOR_MISSING"
    if not row["readout_tau"]:
        return "REFUSED_READOUT_TAU_MISSING"
    if row["mixed_basis"]:
        return "REFUSED_MIXED_BRANCH_OR_BASIS"
    if row["tau_unity"]:
        return "REFUSED_TAU_UNITY_SHORTCUT"
    if row["uses_cancellation"]:
        return "REFUSED_CANCELLATION_ONLY"
    return "COUNTERFACTUAL_FINITE_READY_NOT_CURRENT_CLAIM"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "case_id": row["case_id"],
            "computed_status": evaluate_dryrun(row),
            "expected_status": row["expected_status"],
            "status_match": evaluate_dryrun(row) == row["expected_status"],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in cases
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG2657_0_zero_theorem", "condition": "parent contraction zero theorem is signed", "current_status": "FAIL_CONTRACTION_ZERO_THEOREM_NOT_PARENT_DERIVED", "source_anchor": f"{OUTPUTS['contraction_zero_attempt'].name}:PCZ2657_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2657_1_finite_pack", "condition": "finite WEP coefficient pack is executable", "current_status": "FAIL_FINITE_WEP_COEFFICIENT_PACK_NOT_EXECUTABLE", "source_anchor": f"{OUTPUTS['finite_coefficient_pack'].name}:FWP2657_7_acceptance", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2657_2_live_imports", "condition": "live imports provide derived-zero or source-backed finite rows without placeholders", "current_status": "FAIL_LIVE_IMPORTS_MISSING_OR_PLACEHOLDER", "source_anchor": OUTPUTS["live_import_audit"].name, "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2657_3_no_shortcuts", "condition": "closure-only zero, bound inversion, DD proxy, mixed basis, tau=1 and cancellation are refused", "current_status": "PASS_GUARDS_ENFORCED_BUT_NONCLAIM", "source_anchor": OUTPUTS["dryrun_results"].name, "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2657_4_verdict", "condition": "parent coupling/source/material contraction supports local-GR/WEP claim", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG2657_0_zero_theorem through CG2657_3_no_shortcuts", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC2657_0_zero", "decision": "DO_NOT_PROMOTE_CONTRACTION_ZERO", "reason": "the double-zero proof is exact conditionally, but neighbourhood quotient descent, ordinary-matter signature, no source-only prefactor and readout silence are not parent-signed", "status": "ZERO_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "open-neighbourhood quotient descent and MOMS parent signature", "valid_for_claim": False},
        {"decision_id": "DEC2657_1_finite", "decision": "FINITE_WEP_COEFFICIENT_PACK_STAGED_NONCLAIM", "reason": "the pack names every factor but C_parent/source/material/readout/tau remain missing or placeholders", "status": "FINITE_ROUTE_ACQUISITION_READY_NOT_SCOREABLE", "next_dependency": "source-backed coefficient rows or theorem-zero certificate", "valid_for_claim": False},
        {"decision_id": "DEC2657_2_next", "decision": "SELECT_2658_NEIGHBOURHOOD_DESCENT_OR_MOMS_SIGNATURE", "reason": "the best leap forward is not more data plumbing; it is the parent theorem that would turn the exact double-zero corollary into a real local-GR/Newton reduction", "status": "NEXT_TARGET_SELECTED", "next_dependency": "2658 neighbourhood quotient descent or MOMS parent action signature", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2657_0_selected",
            "status": "selected",
            "next_doc": "2658-Y5-R2FR-neighbourhood-quotient-descent-or-MOMS-parent-signature-source-map.md",
            "next_script": "scripts/Y5_R2FR_neighbourhood_quotient_descent_or_MOMS_parent_signature_source_map_2658.py",
            "target": "Try to parent-sign open-neighbourhood quotient descent and the minimal ordinary-matter signature clauses needed for C_parent double-zero; if not, keep finite C_parent/source rows as explicit nonclaim debt.",
            "must_include": "open fibre neighbourhood; V_WEP verticality; ordinary matter action-density line; no w_A/source-only slot; no hidden spurion/non-Hilbert/readout reentry; finite source map fallback",
            "must_exclude": "closure-only zero, MICROSCOPE bound inversion, DD proxy as parent ontology, tau=1, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT2657_0_theory", "area": "parent contraction theorem", "summary": "the WEP/local-GR branch now has an exact contraction-zero theorem shape, but parent signatures are still missing", "risk_level": "PROMISING_CONDITIONAL_NOT_CLAIMABLE", "project_meaning": "this is real progress: the bridge to GR/Newton is a named theorem target, not an empirical patch", "next_action": "prove neighbourhood quotient descent and MOMS signature", "valid_for_claim": False},
        {"status_id": "STAT2657_1_finite", "area": "finite WEP coefficient pack", "summary": "finite fallback is staged with all required factors and no shortcut permissions", "risk_level": "NONCLAIM_ACQUISITION_READY", "project_meaning": "if the zero theorem fails, the theory still has a disciplined finite-residual branch rather than a fudge factor", "next_action": "source C_parent/source/material/readout/tau or keep blocked", "valid_for_claim": False},
        {"status_id": "STAT2657_2_project_overview", "area": "GR/Newton reduction bridge", "summary": "we are not circling now: the next bottleneck is the parent matter signature that decides whether local ordinary matter is universal", "risk_level": "HARD_CORE_DERIVATION_GATE", "project_meaning": "this is exactly the kind of theorem that could turn the framework from phenomenology into a serious field-theory candidate", "next_action": "2658 neighbourhood quotient descent or MOMS source map", "valid_for_claim": False},
    ]


def branch_copy_rows(zero_rows: list[dict[str, Any]], pack_rows: list[dict[str, Any]], gate_rows: list[dict[str, Any]], dry_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    write_csv(BRANCH_COPIES["queue"], pack_rows)
    write_csv(BRANCH_COPIES["local_bounds"], gate_rows)
    write_csv(BRANCH_COPIES["source_weight"], pack_rows)
    write_csv(BRANCH_COPIES["microscope"], zero_rows)
    write_csv(BRANCH_COPIES["quarantine"], dry_rows)
    return [
        {"copy_id": copy_id, "path": str(path), "exists": path.exists(), "parseable_csv": path.exists() and len(csv_rows(path)) >= 1, "purpose": "2657 parent contraction theorem / finite coefficient pack nonclaim handoff", "valid_for_claim": False}
        for copy_id, path in BRANCH_COPIES.items()
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    zero = contraction_zero_attempt_rows()
    pack = finite_coefficient_pack_rows()
    gates = coefficient_pack_gate_rows()
    dry_cases = dryrun_case_rows()
    dry = dryrun_result_rows(dry_cases)
    rows = {
        "source_register": source_register_rows(),
        "live_import_audit": live_import_audit_rows(),
        "contraction_zero_attempt": zero,
        "finite_coefficient_pack": pack,
        "coefficient_pack_gate": gates,
        "dryrun_cases": dry_cases,
        "dryrun_results": dry,
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }
    rows["branch_copies"] = branch_copy_rows(zero, pack, gates, dry)
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            csv_rows(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2657-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2657*",
        "*Y5_R2FR_parent_coupling_source_material_contraction_zero_or_finite_WEP_coefficient_pack_2657*",
        "*JR2657*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    live_ok = any(row["audit_id"] == "LIA2657_C_parent_placeholder" and row["audit_status"] == "PLACEHOLDER_FILE_EXISTS_NONCLAIM" for row in rows["live_import_audit"]) and any(row["audit_id"] == "LIA2657_C_parent_WEP_slot_import" and row["audit_status"] == "LIVE_IMPORT_MISSING" for row in rows["live_import_audit"])
    zero_ok = any(row["attempt_id"] == "PCZ2657_5_verdict" and row["status"] == "CONTRACTION_ZERO_THEOREM_NOT_PARENT_DERIVED" for row in rows["contraction_zero_attempt"])
    pack_ok = any(row["pack_id"] == "FWP2657_7_acceptance" and row["current_status"] == "FINITE_WEP_COEFFICIENT_PACK_NOT_EXECUTABLE" for row in rows["finite_coefficient_pack"]) and all(not row["score_ready"] and not row["valid_prediction_row"] for row in rows["finite_coefficient_pack"])
    gate_ok = any(row["gate_id"] == "CPG2657_5_verdict" and row["current_status"] == "FINITE_WEP_COEFFICIENT_PACK_NOT_EXECUTABLE" for row in rows["coefficient_pack_gate"]) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["coefficient_pack_gate"])
    dry_ok = all(row["status_match"] and not row["claim_allowed"] for row in rows["dryrun_results"])
    claim_ok = any(row["gate_id"] == "CG2657_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and all(not row["gate_pass"] for row in rows["claim_gates"])
    next_ok = any("2658-Y5-R2FR-neighbourhood-quotient-descent" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2657_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2657_01_live_imports", live_ok, "C_parent placeholder exists but live C_parent_WEP import remains missing"),
        ("VAL2657_02_zero_theorem", zero_ok, "contraction zero theorem is exact conditional but not parent-derived"),
        ("VAL2657_03_finite_pack", pack_ok, "finite WEP coefficient pack is nonclaim/not score-ready"),
        ("VAL2657_04_pack_gates", gate_ok, "coefficient pack executability gates all block claim"),
        ("VAL2657_05_dryrun", dry_ok, "dry-run refuses unsigned zero, closure zero, bound inversion, DD proxy, placeholders, missing factors, tau=1, mixed basis and cancellation"),
        ("VAL2657_06_claim_gates_false", claim_ok, "claim remains blocked"),
        ("VAL2657_07_next_target", next_ok, "2658 neighbourhood quotient descent target is recorded"),
        ("VAL2657_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2657_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2657_10_formalization_untouched", formal_ok, "no 2657 outputs are written under formalization-workbench"),
        ("VAL2657_11_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = stamp()
    out = [
        {"timestamp_utc": generated, "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "valid_for_claim": False, "claim_allowed": False, "validation_id": validation_id, "status": "PASS" if passed else "FAIL", "detail": detail}
        for validation_id, passed, detail in checks
    ]
    out.append(
        {"timestamp_utc": generated, "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "valid_for_claim": False, "claim_allowed": False, "validation_id": "VAL2657_OVERALL", "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL", "detail": "2657 stages exact parent contraction zero theorem, keeps finite WEP coefficient pack nonclaim, and selects neighbourhood quotient descent/MOMS signature next"}
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 2657 - Parent Coupling Source Material Contraction Zero Or Finite WEP Coefficient Pack

## Purpose

This checkpoint attacks the coupling bottleneck directly. It asks whether the WEP source/material contraction vanishes because ordinary matter descends through the parent quotient, or whether the finite WEP branch must stay as an explicit coefficient/input pack.

## Result

- The contraction-zero route is mathematically sharp: if `C_parent_X` is zero for every active WEP channel before readout, the MICROSCOPE/WEP product vanishes.
- The exact double-zero theorem remains conditional: open-neighbourhood quotient descent, ordinary-matter signature, no source-only prefactor, source-current owner and readout silence are not parent-signed.
- The finite WEP coefficient pack is staged but non-executable: `C_parent`, `R_material`, `R_source`, `K_CMSM/tau_eff`, and same-branch product units remain missing or placeholder.
- Existing `C_parent.csv` is useful as a refusal file only; no live `C_parent_WEP_slot_import.csv` exists.
- The next target is 2658: parent-sign neighbourhood quotient descent / MOMS ordinary-matter signature, or keep the finite source map as explicit nonclaim debt.

## Source Register

{markdown_table(rows["source_register"])}

## Live Import Audit

{markdown_table(rows["live_import_audit"])}

## Contraction Zero Theorem Attempt

{markdown_table(rows["contraction_zero_attempt"])}

## Finite WEP Coefficient Pack

{markdown_table(rows["finite_coefficient_pack"])}

## Coefficient Pack Executability Gate

{markdown_table(rows["coefficient_pack_gate"])}

## Dry-Run Cases

{markdown_table(rows["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows["dryrun_results"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows = build_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()
