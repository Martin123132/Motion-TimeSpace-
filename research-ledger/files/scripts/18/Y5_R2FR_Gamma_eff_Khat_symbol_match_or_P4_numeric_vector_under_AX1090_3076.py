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
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3076"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3076-Y5-R2FR-Gamma-eff-Khat-symbol-match-or-P4-numeric-vector-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3076_00_3075_doc": ROOT / "3075-Y5-R2FR-parent-field-inventory-no-independent-Gamma-or-P4-vector-under-AX1090.md",
    "SRC3076_01_3075_next": RESIDUALS / "P8_Y5_R2FR_3075_NEXT_TARGET.csv",
    "SRC3076_02_3075_inventory": RESIDUALS / "P8_Y5_R2FR_3075_PARENT_FIELD_INVENTORY_AUDIT.csv",
    "SRC3076_03_3075_p4": RESIDUALS / "P8_Y5_R2FR_3075_P4_CONNECTION_VECTOR_NONCLAIM.csv",
    "SRC3076_04_3074_symbol": RESIDUALS / "P8_Y5_R2FR_3074_GAMMA_KHAT_SYMBOL_MATCH_LEDGER.csv",
    "SRC3076_05_776_kgamma": RESIDUALS / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
    "SRC3076_06_1289_derivative": RESIDUALS / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "SRC3076_07_metric_contract": RESIDUALS / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
    "SRC3076_08_3065_gamma_owner": RESIDUALS / "P8_Y5_R2FR_3065_GAMMA_EFF_DENSITY_OWNER_GATE.csv",
    "SRC3076_09_3065_khat_identity": RESIDUALS / "P8_Y5_R2FR_3065_KHAT_METRIC_RESPONSE_IDENTITY_AUDIT.csv",
    "SRC3076_10_3065_deltak_rows": RESIDUALS / "P8_Y5_R2FR_3065_DELTAK_INPUT_ROWS_NONCLAIM.csv",
    "SRC3076_11_3009_symbol_audit": RESIDUALS / "P8_Y5_R2FR_3009_REAL_SYMBOL_MATCH_AUDIT.csv",
    "SRC3076_12_3009_deltak": RESIDUALS / "P8_Y5_R2FR_3009_DELTA_K_OBSTRUCTION_DECOMPOSITION.csv",
    "SRC3076_13_2941_action_gate": RESIDUALS / "P8_Y5_R2FR_2941_GK_ACTION_EXISTENCE_THEOREM_GATE.csv",
    "SRC3076_14_2941_helmholtz": RESIDUALS / "P8_Y5_R2FR_2941_HELMHOLTZ_STRONG_ADOPTION_GATE.csv",
    "SRC3076_15_2941_parent_adoption": RESIDUALS / "P8_Y5_R2FR_2941_PARENT_ACTION_ADOPTION_GATE.csv",
    "SRC3076_16_2975_sign_lock": RESIDUALS / "P8_Y5_R2FR_2975_GAMMAKHAT_SIGN_CONVENTION_LOCK.csv",
    "SRC3076_17_2975_certificate": RESIDUALS / "P8_Y5_R2FR_2975_METRIC_RESPONSE_CERTIFICATE_AUDIT.csv",
    "SRC3076_18_2218_tensor_comparison": RESIDUALS / "P8_Y5_PARENT_QLOC_2218_KMETRIC_KHAT_TENSOR_COMPARISON.csv",
    "SRC3076_19_2218_helmholtz": RESIDUALS / "P8_Y5_PARENT_QLOC_2218_HELMHOLTZ_GATE.csv",
    "SRC3076_20_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3076_SOURCE_REGISTER.csv",
    "gamma_owner": RESIDUALS / "P8_Y5_R2FR_3076_GAMMA_EFF_OWNER_AUDIT.csv",
    "khat_match": RESIDUALS / "P8_Y5_R2FR_3076_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "deltak": RESIDUALS / "P8_Y5_R2FR_3076_DELTAK_OBSTRUCTION_VECTOR_NONCLAIM.csv",
    "gk_action": RESIDUALS / "P8_Y5_R2FR_3076_GK_ACTION_ADOPTION_GATE.csv",
    "p4_queue": RESIDUALS / "P8_Y5_R2FR_3076_P4_NUMERIC_VECTOR_QUEUE_NONCLAIM.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3076_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3076_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3076_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3076_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3076_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "gamma_owner_copy": PARENT_ACTION / "Gamma_eff_owner_audit_3076_NOT_SIGNED.csv",
    "khat_match_copy": PARENT_ACTION / "Khat_metric_response_match_3076_NOT_SIGNED.csv",
    "deltak_copy": LOCAL_BOUNDS / "DeltaK_obstruction_vector_3076_NONCLAIM.csv",
    "p4_queue_copy": LOCAL_BOUNDS / "P4_numeric_vector_queue_3076_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3076_DeltaK_component_birth_certificate_or_P4_numeric_NEXT_NONCLAIM.csv",
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
        "owner_signed",
        "identity_signed",
        "gate_signed",
        "parent_adopted",
        "match_signed",
        "local_gr_claim",
        "khat_claim",
        "q_loc_zero_claim",
        "p4_ready",
        "numeric_ready",
        "bound_ready",
        "theorem_zero_signed",
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
            "role": "Gamma_eff_Khat_symbol_match_evidence" if source_id != "SRC3076_20_dotg_target" else "append_guard_target",
            "status": "PRESENT" if source_path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, source_path in SOURCE_PATHS.items()
]

gamma_owner_rows = [
    base(
        {
            "owner_id": "GEO3076_0_live_symbol_role",
            "object": "Gamma_eff",
            "required_contract": "Gamma_eff must be a single parent scalar-density input Gamma_eff(g,Phi,nabla Phi,D,branch), not a fitted readout or route label.",
            "current_status": "NOT_LIVE_SCALAR_DENSITY_OWNER",
            "owner_signed": "false",
            "what_survives": "the scalar-density slot and response-doublet candidate remain coherent",
            "missing_for_claim": "MISSING_PARENT_DENSITY_FORMULA;MISSING_FIELD_CONTENT;MISSING_NO_DATA_FIT_SELECTOR",
            "source_ids": "SRC3076_07_metric_contract;SRC3076_08_3065_gamma_owner;SRC3076_11_3009_symbol_audit",
        }
    ),
    base(
        {
            "owner_id": "GEO3076_1_density_ansatz",
            "object": "sqrt(-g) Gamma_eff",
            "required_contract": "A declared local density with branch domain, units, metric dependence and variation convention.",
            "current_status": "FORMAL_RESPONSE_DOUBLET_CANDIDATE_ONLY",
            "owner_signed": "false",
            "what_survives": "Gamma_eff = Gamma0 + 1/2 M_AB Z^A Z^B + O(Z^4) remains a useful candidate route",
            "missing_for_claim": "MISSING_PARENT_ADOPTION;MISSING_UNITS;MISSING_METRIC_DEPENDENCE;MISSING_BRANCH_DOMAIN",
            "source_ids": "SRC3076_08_3065_gamma_owner;SRC3076_13_2941_action_gate",
        }
    ),
    base(
        {
            "owner_id": "GEO3076_2_background_subtraction",
            "object": "Gamma0/background term",
            "required_contract": "Constant Gamma_eff background is Lambda/EH-compatible and locally silent after subtraction.",
            "current_status": "BACKGROUND_SUBTRACTION_NOT_PARENT_SIGNED",
            "owner_signed": "false",
            "what_survives": "the needed subtraction rule is named",
            "missing_for_claim": "MISSING_EH_LAMBDA_COMPATIBILITY;MISSING_BOUNDARY_CONVENTION;MISSING_READOUT_SUBTRACTION_RULE",
            "source_ids": "SRC3076_07_metric_contract;SRC3076_08_3065_gamma_owner",
        }
    ),
    base(
        {
            "owner_id": "GEO3076_3_MAB_Z_lock",
            "object": "M_AB and Z^A",
            "required_contract": "M_AB is sourced, unitful and positive on the physical quotient-vertical residual basis Z^A.",
            "current_status": "MISSING_MAB_OWNER_AND_Z_BASIS_LOCK",
            "owner_signed": "false",
            "what_survives": "formal Hessian extraction is available once a parent density exists",
            "missing_for_claim": "MISSING_MAB_SOURCE;MISSING_POSITIVITY;MISSING_GAUGE_CONSTRAINT_REMOVAL;MISSING_PHYSICAL_Z_BASIS",
            "source_ids": "SRC3076_08_3065_gamma_owner",
        }
    ),
    base(
        {
            "owner_id": "GEO3076_4_verdict",
            "object": "Gamma_eff owner",
            "required_contract": "All density-owner clauses close in the same branch before Khat can be identified as its metric response.",
            "current_status": "OWNER_NOT_SIGNED_RETAIN_RESIDUAL",
            "owner_signed": "false",
            "what_survives": "Gamma_eff is now constrained to either become a parent density or stay in the residual ledger",
            "missing_for_claim": "MISSING_LIVE_PARENT_DENSITY;MISSING_COMPONENT_CERTIFICATE;MISSING_UNITS_AND_BACKGROUND",
            "source_ids": "SRC3076_04_3074_symbol;SRC3076_08_3065_gamma_owner;SRC3076_11_3009_symbol_audit",
        }
    ),
]

khat_match_rows = [
    base(
        {
            "match_id": "KMR3076_0_formal_Kmetric",
            "target": "K_metric[Gamma_eff]",
            "required_identity": "K_metric^{mu nu}=2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} under the canonical q_loc-positive sign convention.",
            "current_evidence": "formal metric variation route exists",
            "current_status": "PASS_FORMAL_STEP_ONLY",
            "identity_signed": "false",
            "residual_if_missing": "none_for_formal_step_but_no_live_claim",
            "source_ids": "SRC3076_09_3065_khat_identity;SRC3076_16_2975_sign_lock",
        }
    ),
    base(
        {
            "match_id": "KMR3076_1_live_Khat_source",
            "target": "live_MTS_Khat",
            "required_identity": "source-signed live K_hat tensor component list in the same branch as Gamma_eff.",
            "current_evidence": "no source-signed live K_hat component list found",
            "current_status": "MISSING_COMPONENT_SOURCE",
            "identity_signed": "false",
            "residual_if_missing": "Delta_K remains uninterpretable component-by-component",
            "source_ids": "SRC3076_09_3065_khat_identity;SRC3076_18_2218_tensor_comparison",
        }
    ),
    base(
        {
            "match_id": "KMR3076_2_tensor_identity",
            "target": "K_hat == K_metric[Gamma_eff]",
            "required_identity": "the symbol K_hat is defined as the same Hilbert metric response of the same Gamma_eff density.",
            "current_evidence": "existing ledgers preserve Delta_K rather than prove zero",
            "current_status": "NOT_MATCHED_TO_CURRENT_SYMBOLS",
            "identity_signed": "false",
            "residual_if_missing": "Delta_K_total",
            "source_ids": "SRC3076_04_3074_symbol;SRC3076_09_3065_khat_identity;SRC3076_12_3009_deltak",
        }
    ),
    base(
        {
            "match_id": "KMR3076_3_00_component",
            "target": "K_hat^{00}",
            "required_identity": "K_hat^{00}=K_metric^{00} with source-normalization, volume and local branch conventions fixed.",
            "current_evidence": "no live component formula for K_hat^{00}",
            "current_status": "MISSING_COMPONENT_FORMULA",
            "identity_signed": "false",
            "residual_if_missing": "DeltaK_00",
            "source_ids": "SRC3076_09_3065_khat_identity;SRC3076_18_2218_tensor_comparison",
        }
    ),
    base(
        {
            "match_id": "KMR3076_4_0i_component",
            "target": "K_hat^{0i}",
            "required_identity": "momentum/shift component of K_hat equals metric response component without hidden current leakage.",
            "current_evidence": "no live component formula for K_hat^{0i}",
            "current_status": "MISSING_COMPONENT_FORMULA",
            "identity_signed": "false",
            "residual_if_missing": "DeltaK_0i",
            "source_ids": "SRC3076_09_3065_khat_identity;SRC3076_18_2218_tensor_comparison",
        }
    ),
    base(
        {
            "match_id": "KMR3076_5_spatial_trace",
            "target": "h_ij K_hat^{ij}",
            "required_identity": "spatial trace of K_hat equals spatial trace of K_metric in the same volume and subtraction convention.",
            "current_evidence": "no current trace formula or fixed volume convention",
            "current_status": "MISSING_TRACE_FORMULA",
            "identity_signed": "false",
            "residual_if_missing": "DeltaK_trace",
            "source_ids": "SRC3076_09_3065_khat_identity;SRC3076_17_2975_certificate",
        }
    ),
    base(
        {
            "match_id": "KMR3076_6_spatial_tracefree",
            "target": "K_hat^{<ij>}",
            "required_identity": "tracefree/shear part of K_hat equals tracefree/shear metric-response part.",
            "current_evidence": "no current tracefree tensor formula",
            "current_status": "MISSING_TF_FORMULA",
            "identity_signed": "false",
            "residual_if_missing": "DeltaK_TF",
            "source_ids": "SRC3076_09_3065_khat_identity;SRC3076_17_2975_certificate",
        }
    ),
    base(
        {
            "match_id": "KMR3076_7_derivative_boundary",
            "target": "derivative, improvement, symplectic and boundary terms",
            "required_identity": "all derivative/domain/Hodge/projector and boundary terms are included in both K_hat and K_metric.",
            "current_evidence": "derivative, Hodge, domain, projector and boundary response terms remain open",
            "current_status": "MISSING_DERIVATIVE_BOUNDARY_FLUX_CONTROL",
            "identity_signed": "false",
            "residual_if_missing": "DeltaK_derivative_boundary",
            "source_ids": "SRC3076_05_776_kgamma;SRC3076_06_1289_derivative;SRC3076_19_2218_helmholtz",
        }
    ),
    base(
        {
            "match_id": "KMR3076_8_helmholtz",
            "target": "Helmholtz/integrability certificate",
            "required_identity": "K_hat components satisfy the integrability conditions for a parent scalar density variation.",
            "current_evidence": "Helmholtz checks are not evaluable without sourced tensor components and boundary convention",
            "current_status": "HELMHOLTZ_NOT_EVALUABLE",
            "identity_signed": "false",
            "residual_if_missing": "DeltaK_integrability",
            "source_ids": "SRC3076_14_2941_helmholtz;SRC3076_19_2218_helmholtz",
        }
    ),
    base(
        {
            "match_id": "KMR3076_9_verdict",
            "target": "Gamma_eff/K_hat symbol match",
            "required_identity": "Gamma_eff owner and K_hat metric response close together under one sign convention.",
            "current_evidence": "only formal variation passes; live owner, components and Helmholtz gates fail",
            "current_status": "SYMBOL_MATCH_NOT_SIGNED",
            "identity_signed": "false",
            "residual_if_missing": "Delta_K retained as official obstruction vector",
            "source_ids": "SRC3076_04_3074_symbol;SRC3076_08_3065_gamma_owner;SRC3076_09_3065_khat_identity",
        }
    ),
]

deltak_rows = [
    base(
        {
            "delta_id": "DK3076_0_total",
            "component": "Delta_K_total",
            "definition": "Delta_K^{mu nu}:=K_hat_live^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "status": "RETAIN_EXPLICIT_NONCLAIM",
            "residual_formula": "q_loc^nu=P_loc(nabla_mu T_metric^{mu nu})-P_loc(nabla_mu Delta_K^{mu nu}) plus projector/connection/domain/boundary terms",
            "source_needed": "live K_hat component map and K_metric component map",
            "observable_links": "local_GR;PPN;R10;clock;WEP;orbital",
            "source_ids": "SRC3076_12_3009_deltak;SRC3076_16_2975_sign_lock",
        }
    ),
    base(
        {
            "delta_id": "DK3076_1_density_owner",
            "component": "DeltaK_density_owner",
            "definition": "defect caused by Gamma_eff not yet being a live parent scalar density",
            "status": "OPEN_OWNER_DEFECT",
            "residual_formula": "epsilon_Gamma_owner_abs",
            "source_needed": "source-backed Gamma_eff formula, units, branch domain, metric dependence and background rule",
            "observable_links": "all_local_tests",
            "source_ids": "SRC3076_08_3065_gamma_owner",
        }
    ),
    base(
        {
            "delta_id": "DK3076_2_00",
            "component": "DeltaK_00",
            "definition": "K_hat^{00}-K_metric^{00}",
            "status": "OPEN_COMPONENT_DEFECT",
            "residual_formula": "epsilon_DeltaK_00_abs",
            "source_needed": "00 component birth certificate and units",
            "observable_links": "Newtonian_potential;PPN_gamma_beta;R10",
            "source_ids": "SRC3076_09_3065_khat_identity;SRC3076_18_2218_tensor_comparison",
        }
    ),
    base(
        {
            "delta_id": "DK3076_3_0i",
            "component": "DeltaK_0i",
            "definition": "K_hat^{0i}-K_metric^{0i}",
            "status": "OPEN_COMPONENT_DEFECT",
            "residual_formula": "epsilon_DeltaK_0i_abs",
            "source_needed": "momentum/shift component birth certificate and hidden-current exclusion",
            "observable_links": "frame_dragging;orbital;PPN_alpha",
            "source_ids": "SRC3076_09_3065_khat_identity;SRC3076_18_2218_tensor_comparison",
        }
    ),
    base(
        {
            "delta_id": "DK3076_4_trace",
            "component": "DeltaK_trace",
            "definition": "h_ij(K_hat^{ij}-K_metric^{ij})",
            "status": "OPEN_COMPONENT_DEFECT",
            "residual_formula": "epsilon_DeltaK_trace_abs",
            "source_needed": "spatial trace formula, volume convention and background subtraction",
            "observable_links": "PPN;clock;cosmology_local_limit",
            "source_ids": "SRC3076_09_3065_khat_identity;SRC3076_17_2975_certificate",
        }
    ),
    base(
        {
            "delta_id": "DK3076_5_tracefree",
            "component": "DeltaK_TF",
            "definition": "tracefree spatial part of K_hat-K_metric",
            "status": "OPEN_COMPONENT_DEFECT",
            "residual_formula": "epsilon_DeltaK_TF_abs",
            "source_needed": "tracefree/shear component formula or theorem-zero",
            "observable_links": "lightcone;tidal;orbital",
            "source_ids": "SRC3076_09_3065_khat_identity;SRC3076_17_2975_certificate",
        }
    ),
    base(
        {
            "delta_id": "DK3076_6_derivative_boundary",
            "component": "DeltaK_derivative_boundary",
            "definition": "difference in derivative, Hodge, projector, improvement, boundary and corner response terms",
            "status": "OPEN_DERIVATIVE_BOUNDARY_DEFECT",
            "residual_formula": "epsilon_DeltaK_derivative_boundary_abs",
            "source_needed": "boundary/no-flux theorem or sourced edge/corner bound plus derivative-domain response map",
            "observable_links": "R10;clock;orbital;operator_domain",
            "source_ids": "SRC3076_05_776_kgamma;SRC3076_06_1289_derivative;SRC3076_19_2218_helmholtz",
        }
    ),
    base(
        {
            "delta_id": "DK3076_7_units_convention",
            "component": "DeltaK_units",
            "definition": "dimension/sign convention mismatch between K_hat and K_metric",
            "status": "SIGN_CONVENTION_LOCKED_UNITS_STILL_OPEN",
            "residual_formula": "epsilon_units_abs if K_hat/K_metric use incompatible normalization",
            "source_needed": "unit ledger for Gamma_eff, K_hat, K_metric and local projection P_loc",
            "observable_links": "all_scoring",
            "source_ids": "SRC3076_16_2975_sign_lock;SRC3076_17_2975_certificate",
        }
    ),
    base(
        {
            "delta_id": "DK3076_8_projector_domain",
            "component": "DeltaK_projector_domain",
            "definition": "defect from applying P_loc, readout windows or domain restrictions after the metric response",
            "status": "OPEN_PROJECTOR_DOMAIN_DEFECT",
            "residual_formula": "epsilon_projector_domain_abs from commutator/readout leakage",
            "source_needed": "P_loc definition, commutator norm/zero theorem and domain descent rule",
            "observable_links": "local_GR;R10;clock;orbital",
            "source_ids": "SRC3076_12_3009_deltak;SRC3076_06_1289_derivative",
        }
    ),
]

gk_action_rows = [
    base(
        {
            "gate_id": "GKA3076_0_weak_action_template",
            "target": "weak S_GK template",
            "requirement": "A formal parent action can produce an A-equation resembling nabla Gamma_eff - nabla Khat - J_M = 0.",
            "current_status": "WEAK_TEMPLATE_EXISTS",
            "weak_pass": "true",
            "gate_signed": "false",
            "parent_adopted": "false",
            "consequence": "useful construction aid, not a live MTS theorem",
            "missing_for_claim": "MISSING_PARENT_ADOPTION;MISSING_LIVE_FIELDS;MISSING_BOUNDARY_RULE",
            "source_ids": "SRC3076_13_2941_action_gate;SRC3076_15_2941_parent_adoption",
        }
    ),
    base(
        {
            "gate_id": "GKA3076_1_scalar_density_owner",
            "target": "Gamma_eff density owner",
            "requirement": "Gamma_eff is a covariant scalar-density input, not a post-readout function.",
            "current_status": "FAILED_CURRENT_SOURCE_SET",
            "weak_pass": "false",
            "gate_signed": "false",
            "parent_adopted": "false",
            "consequence": "q_loc remains residual-owned",
            "missing_for_claim": "MISSING_PARENT_DENSITY_FORMULA",
            "source_ids": "SRC3076_07_metric_contract;SRC3076_08_3065_gamma_owner",
        }
    ),
    base(
        {
            "gate_id": "GKA3076_2_Khat_metric_response",
            "target": "K_hat metric response",
            "requirement": "K_hat equals the Hilbert metric response of the same Gamma_eff density including derivative and boundary terms.",
            "current_status": "FAILED_CURRENT_SOURCE_SET",
            "weak_pass": "false",
            "gate_signed": "false",
            "parent_adopted": "false",
            "consequence": "Gamma_eff and K_hat cannot yet be treated as one variational object",
            "missing_for_claim": "MISSING_COMPONENT_CERTIFICATE;MISSING_HELMHOLTZ_CHECK",
            "source_ids": "SRC3076_07_metric_contract;SRC3076_09_3065_khat_identity;SRC3076_14_2941_helmholtz",
        }
    ),
    base(
        {
            "gate_id": "GKA3076_3_Ward_identity",
            "target": "q_loc Ward residual",
            "requirement": "diffeomorphism invariance of the same action gives q_loc with only Euler/boundary/projector residuals.",
            "current_status": "CONDITIONAL_NOT_LIVE",
            "weak_pass": "false",
            "gate_signed": "false",
            "parent_adopted": "false",
            "consequence": "Ward route remains possible but not owned by current symbols",
            "missing_for_claim": "MISSING_PARENT_ACTION;MISSING_DELTAK_ZERO_OR_BOUND;MISSING_PLOC_MAP",
            "source_ids": "SRC3076_07_metric_contract;SRC3076_13_2941_action_gate",
        }
    ),
    base(
        {
            "gate_id": "GKA3076_4_Euler_silence",
            "target": "local source-free field equations",
            "requirement": "fields entering Gamma_eff obey positive source-free local equations in compact local vacuum.",
            "current_status": "NOT_SIGNED",
            "weak_pass": "false",
            "gate_signed": "false",
            "parent_adopted": "false",
            "consequence": "physical local force residual may remain",
            "missing_for_claim": "MISSING_EULER_EQUATIONS;MISSING_POSITIVITY;MISSING_BOUNDARY_CONDITIONS",
            "source_ids": "SRC3076_07_metric_contract;SRC3076_15_2941_parent_adoption",
        }
    ),
    base(
        {
            "gate_id": "GKA3076_5_fixed_point_subtraction",
            "target": "fixed-point background subtraction",
            "requirement": "constant Gamma_eff(Phi0) is absorbed into Lambda/background subtraction and produces no local force.",
            "current_status": "NOT_PARENT_SIGNED",
            "weak_pass": "false",
            "gate_signed": "false",
            "parent_adopted": "false",
            "consequence": "constant background contamination remains possible",
            "missing_for_claim": "MISSING_EH_COMPATIBILITY;MISSING_SUBTRACTION_CONVENTION;MISSING_NO_FLUX_BOUNDARY",
            "source_ids": "SRC3076_07_metric_contract;SRC3076_08_3065_gamma_owner",
        }
    ),
    base(
        {
            "gate_id": "GKA3076_6_double_zero",
            "target": "first variation silence",
            "requirement": "partial_A T_GK^{mu nu}(Phi0)=0 for the physical residual directions.",
            "current_status": "FORMAL_ROUTE_ONLY",
            "weak_pass": "false",
            "gate_signed": "false",
            "parent_adopted": "false",
            "consequence": "linear PPN/fifth-force/source-normalization leakage remains possible",
            "missing_for_claim": "MISSING_PHYSICAL_Z_BASIS;MISSING_MAB_OWNER;MISSING_SOURCE_READOUT_EVENNESS",
            "source_ids": "SRC3076_07_metric_contract;SRC3076_08_3065_gamma_owner",
        }
    ),
    base(
        {
            "gate_id": "GKA3076_7_verdict",
            "target": "strong GK action adoption",
            "requirement": "all GK action gates pass in one live branch.",
            "current_status": "STRONG_ADOPTION_FAILS_CURRENT_SOURCE_SET",
            "weak_pass": "false",
            "gate_signed": "false",
            "parent_adopted": "false",
            "consequence": "no q_loc zero, local-GR, PPN, R10, clock, WEP or orbital claim",
            "missing_for_claim": "MISSING_GAMMA_OWNER;MISSING_KHAT_MATCH;MISSING_EULER_SILENCE;MISSING_BOUNDARY_DOMAIN_PROJECTOR_CONTROL",
            "source_ids": "SRC3076_13_2941_action_gate;SRC3076_14_2941_helmholtz;SRC3076_15_2941_parent_adoption",
        }
    ),
]

p4_queue_rows = [
    base(
        {
            "queue_id": "P4Q3076_0_TQ_combined",
            "component": "K_P4_TQ",
            "symbolic_bound": "K_P4_TQ <= c_T T_bar + c_Q Q_bar",
            "status": "SOURCE_OR_THEOREM_ZERO_REQUIRED_NONCLAIM",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_C_T;MISSING_T_BAR;MISSING_C_Q;MISSING_Q_BAR;MISSING_WEAK_FIELD_MAP",
            "observable_links": "WEP;clock;lightcone;operator_domain",
            "next_source_task": "source torsion/nonmetricity weak-field coefficients or prove no-independent-Gamma",
            "source_ids": "SRC3076_03_3075_p4",
        }
    ),
    base(
        {
            "queue_id": "P4Q3076_1_spin",
            "component": "K_P4_spin",
            "symbolic_bound": "K_P4_spin <= c_spin S_axial_bar",
            "status": "SOURCE_OR_THEOREM_ZERO_REQUIRED_NONCLAIM",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_C_SPIN;MISSING_SPINOR_ASSUMPTIONS;MISSING_S_AXIAL_BAR",
            "observable_links": "spin;clock;operator_domain",
            "next_source_task": "source spin/torsion assumptions or prove matter action carries no independent connection current",
            "source_ids": "SRC3076_03_3075_p4",
        }
    ),
    base(
        {
            "queue_id": "P4Q3076_2_projective",
            "component": "K_P4_proj",
            "symbolic_bound": "K_P4_proj <= c_proj P_projective_bar",
            "status": "SOURCE_OR_THEOREM_ZERO_REQUIRED_NONCLAIM",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_PROJECTIVE_INVARIANCE_OR_C_PROJ;MISSING_P_PROJECTIVE_BAR",
            "observable_links": "WEP;operator_domain",
            "next_source_task": "prove projective silence or source projective leakage coefficient",
            "source_ids": "SRC3076_03_3075_p4",
        }
    ),
    base(
        {
            "queue_id": "P4Q3076_3_weyl_nonmetricity",
            "component": "K_P4_QW",
            "symbolic_bound": "K_P4_QW <= c_QW Q_W_bar",
            "status": "SOURCE_OR_THEOREM_ZERO_REQUIRED_NONCLAIM",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_C_QW;MISSING_Q_W_BAR;MISSING_CLOCK_ROD_MAP",
            "observable_links": "clock;rod_calibration;WEP",
            "next_source_task": "source Weyl nonmetricity clock/rod coupling or prove metric-only descent",
            "source_ids": "SRC3076_03_3075_p4",
        }
    ),
    base(
        {
            "queue_id": "P4Q3076_4_shear_nonmetricity",
            "component": "K_P4_QTF",
            "symbolic_bound": "K_P4_QTF <= c_QTF Q_TF_bar",
            "status": "SOURCE_OR_THEOREM_ZERO_REQUIRED_NONCLAIM",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_C_QTF;MISSING_Q_TF_BAR;MISSING_LIGHTCONE_MAP",
            "observable_links": "lightcone;clock;WEP;orbital",
            "next_source_task": "source tracefree nonmetricity lightcone response or prove local silence",
            "source_ids": "SRC3076_03_3075_p4",
        }
    ),
    base(
        {
            "queue_id": "P4Q3076_5_hypermomentum",
            "component": "K_P4_H",
            "symbolic_bound": "K_P4_H <= c_H H_bar",
            "status": "SOURCE_OR_THEOREM_ZERO_REQUIRED_NONCLAIM",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_NO_HYPERMOMENTUM_THEOREM;MISSING_C_H;MISSING_H_BAR",
            "observable_links": "WEP;clock;spin;lightcone;operator_domain",
            "next_source_task": "prove no-hypermomentum or source hypermomentum residual coefficient",
            "source_ids": "SRC3076_03_3075_p4",
        }
    ),
    base(
        {
            "queue_id": "P4Q3076_6_total",
            "component": "K_P4_bar",
            "symbolic_bound": "K_P4_bar := K_P4_TQ + K_P4_spin + K_P4_proj + K_P4_QW + K_P4_QTF + K_P4_H",
            "status": "P4_QUEUE_NONCLAIM",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_ALL_COMPONENT_BOUNDS;MISSING_COMMON_UNITS;MISSING_ARENA_PROJECTIONS",
            "observable_links": "local_GR;PPN;R10;clock;WEP;orbital",
            "next_source_task": "only score after DeltaK component certificate attempt or no-independent-Gamma theorem fails again",
            "source_ids": "SRC3076_03_3075_p4;SRC3076_02_3075_inventory",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3076_0_symbol_match",
            "decision": "Gamma_eff/K_hat symbol match not signed",
            "reason": "Gamma_eff owner, live Khat component list, tensor identity and Helmholtz certificate are all unsigned",
            "consequence": "do not identify K_hat with K_metric[Gamma_eff]",
            "next_action": "retain Delta_K obstruction vector",
        }
    ),
    base(
        {
            "decision_id": "DEC3076_1_weak_action",
            "decision": "weak GK action template remains useful but nonclaim",
            "reason": "formal action construction exists, but live parent adoption and boundary/domain/projector clauses fail",
            "consequence": "no q_loc zero or local-GR theorem",
            "next_action": "use the weak template as a contract for future parent action terms",
        }
    ),
    base(
        {
            "decision_id": "DEC3076_2_P4_queue",
            "decision": "P4 numeric/theorem-zero queue retained",
            "reason": "3075 P4 fallback is still required if no-independent-Gamma/no-hypermomentum stays unsigned",
            "consequence": "P4 cannot be hidden inside K_conn",
            "next_action": "source P4 components only after attempting the Delta_K component birth certificate",
        }
    ),
    base(
        {
            "decision_id": "DEC3076_3_next",
            "decision": "3077 DeltaK component birth certificate",
            "reason": "the cleanest route to GR reduction is now component-level: 00, 0i, trace, tracefree, derivative/boundary and units",
            "consequence": "either Delta_K becomes theorem-zero/bounded or local branch remains residual-scored",
            "next_action": "3077-Y5-R2FR-DeltaK-component-birth-certificate-or-P4-numeric-source-fill-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3076_0_Gamma_owner",
            "claim": "Gamma_eff is a live parent scalar density",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "density route is coherent but not parent-signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3076_1_Khat_identity",
            "claim": "K_hat equals K_metric[Gamma_eff]",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "component certificate and Helmholtz gate are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3076_2_q_loc_zero",
            "claim": "q_loc^nu vanishes in local vacuum",
            "claim_active": "false",
            "status": "BLOCKED_BY_DELTAK_AND_PROJECTORS",
            "reason": "Delta_K, P_loc, domain and boundary terms remain physical residual channels",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3076_3_local_tests",
            "claim": "local GR/Newton/PPN/R10/clock/WEP/orbital pass",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "no local arena is allowed to pass while Delta_K and P4 queues are nonclaim",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3076_0_3077",
            "next_checkpoint": "3077-Y5-R2FR-DeltaK-component-birth-certificate-or-P4-numeric-source-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_DeltaK_component_birth_certificate_or_P4_numeric_source_fill_under_AX1090_3077.py",
            "mission": "try to source the live Khat component certificate for 00, 0i, trace, tracefree, derivative/boundary and units; if that fails, start P4 numeric/theorem-zero source rows",
            "starting_equation": "q_loc^nu=P_loc(nabla_mu T_metric^{mu nu})-P_loc(nabla_mu Delta_K^{mu nu}) plus P4/domain/boundary terms",
            "claim_policy": "no local-GR claim unless Delta_K is theorem-zero/bounded and P4, P_loc, domain, boundary and units close",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["gamma_owner"], gamma_owner_rows)
write_csv(OUTPUTS["khat_match"], khat_match_rows)
write_csv(OUTPUTS["deltak"], deltak_rows)
write_csv(OUTPUTS["gk_action"], gk_action_rows)
write_csv(OUTPUTS["p4_queue"], p4_queue_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["gamma_owner"], BRANCH_OUTPUTS["gamma_owner_copy"])
copy_csv(OUTPUTS["khat_match"], BRANCH_OUTPUTS["khat_match_copy"])
copy_csv(OUTPUTS["deltak"], BRANCH_OUTPUTS["deltak_copy"])
copy_csv(OUTPUTS["p4_queue"], BRANCH_OUTPUTS["p4_queue_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(source_path),
            "copy_path": str(destination_path),
            "copy_exists": str(destination_path.exists()),
            "copy_parse_ok": str(csv_ok(destination_path)),
            "status": "COPIED_NONCLAIM",
        }
    )
    for copy_id, source_path, destination_path in [
        ("BC3076_0_gamma_owner", OUTPUTS["gamma_owner"], BRANCH_OUTPUTS["gamma_owner_copy"]),
        ("BC3076_1_khat_match", OUTPUTS["khat_match"], BRANCH_OUTPUTS["khat_match_copy"]),
        ("BC3076_2_deltak", OUTPUTS["deltak"], BRANCH_OUTPUTS["deltak_copy"]),
        ("BC3076_3_p4_queue", OUTPUTS["p4_queue"], BRANCH_OUTPUTS["p4_queue_copy"]),
        ("BC3076_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)
write_csv(
    OUTPUTS["validation"],
    [
        base(
            {
                "validation_id": "VAL3076_PRE",
                "passed": "False",
                "requirement": "placeholder overwritten by final validation",
                "evidence": "generator ordering guard",
            }
        )
    ],
)
DOC.write_text("# 3076 draft\n", encoding="utf-8")

remove_pycache()
dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
generated_rows = (
    gamma_owner_rows
    + khat_match_rows
    + deltak_rows
    + gk_action_rows
    + p4_queue_rows
    + decision_rows
    + claim_rows
    + next_rows
)
formalization_output_count = sum(1 for output_path in generated_csvs + [DOC] if under(output_path, FORMALIZATION))

validation_rows = [
    base(
        {
            "validation_id": "VAL3076_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3076_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3076_02_csv_parse",
            "passed": str(all(csv_ok(output_path) for output_path in generated_csvs)),
            "requirement": "all generated and branch-copy CSVs parse cleanly",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3076_03_gamma_owner_not_signed",
            "passed": str(not any(boolish(row["owner_signed"]) for row in gamma_owner_rows)),
            "requirement": "Gamma_eff owner remains unsigned",
            "evidence": OUTPUTS["gamma_owner"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3076_04_khat_match_not_signed",
            "passed": str(not any(boolish(row["identity_signed"]) for row in khat_match_rows)),
            "requirement": "K_hat metric response match remains unsigned",
            "evidence": OUTPUTS["khat_match"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3076_05_weak_GK_not_promoted",
            "passed": str(any(row["current_status"] == "WEAK_TEMPLATE_EXISTS" for row in gk_action_rows) and not any(boolish(row["gate_signed"]) or boolish(row["parent_adopted"]) for row in gk_action_rows)),
            "requirement": "weak GK action template is acknowledged but not promoted to a live claim",
            "evidence": OUTPUTS["gk_action"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3076_06_DeltaK_vector_retained",
            "passed": str(any(row["component"] == "Delta_K_total" for row in deltak_rows) and not has_claim_true(deltak_rows)),
            "requirement": "Delta_K obstruction vector is retained as nonclaim",
            "evidence": OUTPUTS["deltak"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3076_07_P4_queue_nonclaim",
            "passed": str(any(row["component"] == "K_P4_bar" for row in p4_queue_rows) and not has_claim_true(p4_queue_rows)),
            "requirement": "P4 numeric/theorem-zero queue is retained as nonclaim",
            "evidence": OUTPUTS["p4_queue"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3076_08_no_local_GR_claim",
            "passed": str(not has_claim_true(claim_rows + decision_rows)),
            "requirement": "no q_loc zero, Khat, local-GR, PPN, R10, clock, WEP or orbital claim is promoted",
            "evidence": OUTPUTS["claim_status"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3076_09_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3077-Y5-R2FR-DeltaK-component-birth-certificate")),
            "requirement": "next target moves to DeltaK component birth certificate or P4 numeric source fill",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3076_10_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3076_11_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3076_12_outputs_under_post_checkpoint",
            "passed": str(all(under(output_path, ROOT) for output_path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3076_13_no_formalization_outputs",
            "passed": str(formalization_output_count == 0),
            "requirement": "formalization-workbench modified-file count for 3076 outputs remains zero",
            "evidence": f"formalization_3076_output_paths={formalization_output_count}",
        }
    ),
    base(
        {
            "validation_id": "VAL3076_14_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3076_15_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
    base(
        {
            "validation_id": "VAL3076_16_sign_convention_inherited",
            "passed": str(any("Delta_K^{mu nu}:=K_hat_live" in row["definition"] for row in deltak_rows)),
            "requirement": "canonical Delta_K convention is inherited from 2975",
            "evidence": OUTPUTS["deltak"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3076_17_DeltaK_components_complete",
            "passed": str({"Delta_K_total", "DeltaK_density_owner", "DeltaK_00", "DeltaK_0i", "DeltaK_trace", "DeltaK_TF", "DeltaK_derivative_boundary", "DeltaK_units", "DeltaK_projector_domain"}.issubset({row["component"] for row in deltak_rows})),
            "requirement": "Delta_K component vector includes owner, 00, 0i, trace, tracefree, derivative/boundary, units and projector/domain rows",
            "evidence": OUTPUTS["deltak"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3076_18_no_claim_fields_true",
            "passed": str(not has_claim_true(generated_rows)),
            "requirement": "no generated non-validation row contains a true claim/ready field",
            "evidence": "claim field scan",
        }
    ),
]

write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3076 - Gamma_eff/Khat Symbol Match or P4 Numeric Vector

Status: `Y5_R2FR_3076_symbol_match_not_signed_DeltaK_vector_written`

Generated: `{RUN_UTC}`

## Verdict

3076 tried the clean derivation move: identify `Gamma_eff` and `K_hat` as two faces of the same parent action term, with `K_hat` equal to the Hilbert metric response of `sqrt(-g) Gamma_eff`.

The formal route still exists and is valuable: a weak `S_GK` template can produce the right kind of Ward/A-equation structure. But the live MTS symbols do not yet close the contract. `Gamma_eff` is not yet a source-signed parent scalar density, `K_hat` is not yet component-certified as `K_metric[Gamma_eff]`, and Helmholtz/boundary/domain/projector terms remain open.

So 3076 does **not** claim `Khat`, `q_loc=0`, local GR, Newtonian recovery, PPN, R10, clocks, WEP, or orbital success.

The gain is sharper than it looks: the obstruction now has a name and components,

`Delta_K^{{mu nu}} := K_hat_live^{{mu nu}} - K_metric^{{mu nu}}[Gamma_eff]`.

Until this vector is theorem-zero or bounded, the local branch is not derivable GR. The next target is therefore component-level: build the `Delta_K` birth certificate before spending tokens on P4 numerics.

## Gamma_eff Owner Audit

{md_table(gamma_owner_rows, ["owner_id", "object", "current_status", "owner_signed", "missing_for_claim"])}

## Khat Metric-Response Match Audit

{md_table(khat_match_rows, ["match_id", "target", "current_status", "identity_signed", "residual_if_missing"])}

## DeltaK Obstruction Vector

{md_table(deltak_rows, ["delta_id", "component", "status", "residual_formula", "source_needed"])}

## GK Action Adoption Gate

{md_table(gk_action_rows, ["gate_id", "target", "current_status", "weak_pass", "gate_signed", "parent_adopted"])}

## P4 Numeric/Theorem-Zero Queue

{md_table(p4_queue_rows, ["queue_id", "component", "status", "symbolic_bound", "missing_for_claim"])}

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
- Gamma_eff owner audit: `{OUTPUTS["gamma_owner"]}`
- Khat metric-response match audit: `{OUTPUTS["khat_match"]}`
- DeltaK obstruction vector: `{OUTPUTS["deltak"]}`
- GK action adoption gate: `{OUTPUTS["gk_action"]}`
- P4 numeric/theorem-zero queue: `{OUTPUTS["p4_queue"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
- Branch copy: `{BRANCH_OUTPUTS["gamma_owner_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["khat_match_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["deltak_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["p4_queue_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["next_copy"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
print(f"Wrote {DOC}")
print(f"Wrote {OUTPUTS['validation']}")
print(f"Validation passed {sum(1 for row in validation_rows if row['passed'] == 'True')}/{len(validation_rows)}")
