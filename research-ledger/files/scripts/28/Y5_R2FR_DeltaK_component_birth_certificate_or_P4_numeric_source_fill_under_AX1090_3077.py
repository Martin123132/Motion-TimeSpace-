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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3077"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3077-Y5-R2FR-DeltaK-component-birth-certificate-or-P4-numeric-source-fill-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3077_00_3076_doc": ROOT / "3076-Y5-R2FR-Gamma-eff-Khat-symbol-match-or-P4-numeric-vector-under-AX1090.md",
    "SRC3077_01_3076_next": RESIDUALS / "P8_Y5_R2FR_3076_NEXT_TARGET.csv",
    "SRC3077_02_3076_deltak": RESIDUALS / "P8_Y5_R2FR_3076_DELTAK_OBSTRUCTION_VECTOR_NONCLAIM.csv",
    "SRC3077_03_3076_khat": RESIDUALS / "P8_Y5_R2FR_3076_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "SRC3077_04_3076_gamma": RESIDUALS / "P8_Y5_R2FR_3076_GAMMA_EFF_OWNER_AUDIT.csv",
    "SRC3077_05_3076_p4": RESIDUALS / "P8_Y5_R2FR_3076_P4_NUMERIC_VECTOR_QUEUE_NONCLAIM.csv",
    "SRC3077_06_2809_components": RESIDUALS / "P8_Y5_R2FR_2809_KHAT_COMPONENT_MATCH_ATTEMPT.csv",
    "SRC3077_07_2218_tensor": RESIDUALS / "P8_Y5_PARENT_QLOC_2218_KMETRIC_KHAT_TENSOR_COMPARISON.csv",
    "SRC3077_08_2409_match": RESIDUALS / "P8_Y5_PARENT_QLOC_2409_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "SRC3077_09_2975_certificate": RESIDUALS / "P8_Y5_R2FR_2975_METRIC_RESPONSE_CERTIFICATE_AUDIT.csv",
    "SRC3077_10_2807_match": RESIDUALS / "P8_Y5_R2FR_2807_GAMMA_KHAT_METRIC_RESPONSE_MATCH.csv",
    "SRC3077_11_2218_helmholtz": RESIDUALS / "P8_Y5_PARENT_QLOC_2218_HELMHOLTZ_GATE.csv",
    "SRC3077_12_1289_derivative": RESIDUALS / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "SRC3077_13_776_kgamma": RESIDUALS / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
    "SRC3077_14_3075_p4": RESIDUALS / "P8_Y5_R2FR_3075_P4_CONNECTION_VECTOR_NONCLAIM.csv",
    "SRC3077_15_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3077_SOURCE_REGISTER.csv",
    "birth_certificate": RESIDUALS / "P8_Y5_R2FR_3077_DELTAK_COMPONENT_BIRTH_CERTIFICATE_AUDIT.csv",
    "khat_source": RESIDUALS / "P8_Y5_R2FR_3077_KHAT_LIVE_COMPONENT_SOURCE_AUDIT.csv",
    "kmetric_requirements": RESIDUALS / "P8_Y5_R2FR_3077_KMETRIC_COMPONENT_REQUIREMENT_LEDGER.csv",
    "helmholtz": RESIDUALS / "P8_Y5_R2FR_3077_HELMHOLTZ_EVALUABILITY_GATE.csv",
    "p4_fill": RESIDUALS / "P8_Y5_R2FR_3077_P4_SOURCE_FILL_QUEUE_NONCLAIM.csv",
    "local_blockers": RESIDUALS / "P8_Y5_R2FR_3077_LOCAL_ARENA_BLOCKER_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3077_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3077_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3077_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3077_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3077_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "birth_certificate_copy": PARENT_ACTION / "DeltaK_component_birth_certificate_3077_NOT_SIGNED.csv",
    "khat_source_copy": PARENT_ACTION / "Khat_live_component_source_audit_3077_MISSING.csv",
    "local_blockers_copy": LOCAL_BOUNDS / "Local_arena_blockers_3077_NONCLAIM.csv",
    "p4_fill_copy": LOCAL_BOUNDS / "P4_source_fill_queue_3077_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3077_P4_TQ_first_source_or_theorem_zero_NEXT_NONCLAIM.csv",
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
        "certificate_signed",
        "component_source_signed",
        "component_match_signed",
        "helmholtz_evaluable",
        "helmholtz_pass",
        "p4_ready",
        "numeric_ready",
        "theorem_zero_signed",
        "arena_pass",
        "local_gr_claim",
        "q_loc_zero_claim",
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
            "role": "DeltaK_component_birth_certificate_evidence" if source_id != "SRC3077_15_dotg_target" else "append_guard_target",
            "status": "PRESENT" if source_path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, source_path in SOURCE_PATHS.items()
]

component_specs = [
    {
        "component": "DeltaK_00",
        "khat_required": "live K_hat^{00} source equation with source-normalization, volume convention and units",
        "kmetric_required": "K_metric^{00}=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_00 including volume and Gamma0 subtraction",
        "observable_links": "Newtonian_potential;PPN_beta_gamma;R10",
        "current_evidence": "no current component formula for K_hat^{00}",
        "source_ids": "SRC3077_06_2809_components;SRC3077_07_2218_tensor;SRC3077_09_2975_certificate",
    },
    {
        "component": "DeltaK_0i",
        "khat_required": "live K_hat^{0i} source equation with momentum/preferred-frame current exclusions",
        "kmetric_required": "K_metric^{0i} response under shift variation, including derivative-current terms",
        "observable_links": "preferred_frame;frame_dragging;orbital",
        "current_evidence": "no current component formula for K_hat^{0i}",
        "source_ids": "SRC3077_06_2809_components;SRC3077_07_2218_tensor",
    },
    {
        "component": "DeltaK_trace",
        "khat_required": "live h_ij K_hat^{ij} source equation with pressure/trace and volume convention",
        "kmetric_required": "spatial trace of K_metric including volume response, M_AB metric dependence and subtraction",
        "observable_links": "PPN;clock;orbital;cosmology_local_limit",
        "current_evidence": "no current trace formula or fixed volume convention",
        "source_ids": "SRC3077_06_2809_components;SRC3077_09_2975_certificate",
    },
    {
        "component": "DeltaK_TF",
        "khat_required": "live tracefree/shear K_hat^{<ij>} formula or theorem-zero improvement channel",
        "kmetric_required": "tracefree/shear metric response including anisotropic derivative terms",
        "observable_links": "lightcone;tidal;orbital;lensing_style_local_tail",
        "current_evidence": "no current tracefree tensor formula; tracefree route remains candidate only",
        "source_ids": "SRC3077_06_2809_components;SRC3077_09_2975_certificate",
    },
    {
        "component": "DeltaK_derivative_boundary",
        "khat_required": "live derivative/improvement/boundary K_hat terms with no-flux or finite edge coefficients",
        "kmetric_required": "metric response of derivative, Hodge, connection, domain, projector and boundary operators",
        "observable_links": "R10;clock;operator_domain;surface_flux",
        "current_evidence": "derivative response and boundary/reference convention not supplied componentwise",
        "source_ids": "SRC3077_06_2809_components;SRC3077_11_2218_helmholtz;SRC3077_12_1289_derivative;SRC3077_13_776_kgamma",
    },
    {
        "component": "DeltaK_units",
        "khat_required": "unit ledger for K_hat stress-density normalization and q_loc projection",
        "kmetric_required": "unit ledger for Gamma_eff, K_metric, P_loc and observable arena map",
        "observable_links": "all_local_scoring",
        "current_evidence": "stress-density and q_loc/readout units are missing",
        "source_ids": "SRC3077_07_2218_tensor;SRC3077_09_2975_certificate",
    },
    {
        "component": "DeltaK_projector_domain",
        "khat_required": "source showing K_hat is computed before/after the same P_loc/domain/readout operation as K_metric",
        "kmetric_required": "commutator or descent theorem for P_loc with divergence and metric variation",
        "observable_links": "local_GR;R10;clock;orbital",
        "current_evidence": "projector/readout/domain commutator remains open",
        "source_ids": "SRC3077_02_3076_deltak;SRC3077_12_1289_derivative",
    },
]

birth_certificate_rows = [
    base(
        {
            "certificate_id": f"DBC3077_{index}_{spec['component']}",
            "component": spec["component"],
            "birth_certificate_required": "same-branch Khat source; same-branch Kmetric source; sign convention; units; boundary/domain convention; observable projection",
            "khat_required": spec["khat_required"],
            "kmetric_required": spec["kmetric_required"],
            "current_evidence": spec["current_evidence"],
            "certificate_status": "BIRTH_CERTIFICATE_NOT_SIGNED",
            "certificate_signed": "false",
            "component_match_signed": "false",
            "residual_if_missing": spec["component"],
            "observable_links": spec["observable_links"],
            "missing_for_claim": "MISSING_LIVE_KHAT_COMPONENT;MISSING_KMETRIC_COMPONENT_VALUE;MISSING_UNITS_OR_DOMAIN_CERTIFICATE",
            "source_ids": spec["source_ids"],
        }
    )
    for index, spec in enumerate(component_specs)
]
birth_certificate_rows.append(
    base(
        {
            "certificate_id": "DBC3077_7_total",
            "component": "Delta_K_total",
            "birth_certificate_required": "all component certificates pass and Helmholtz/boundary/domain gates are evaluable",
            "khat_required": "complete live K_hat tensor map",
            "kmetric_required": "complete K_metric tensor map from the same Gamma_eff density",
            "current_evidence": "no component certificate closes",
            "certificate_status": "TOTAL_CERTIFICATE_FAILS_CURRENT_SOURCE_SET",
            "certificate_signed": "false",
            "component_match_signed": "false",
            "residual_if_missing": "Delta_K_total",
            "observable_links": "local_GR;Newton;PPN;R10;clock;WEP;orbital",
            "missing_for_claim": "MISSING_ALL_COMPONENT_CERTIFICATES;MISSING_HELMHOLTZ;MISSING_P4_AND_PLOC_CLOSURE",
            "source_ids": "SRC3077_02_3076_deltak;SRC3077_03_3076_khat;SRC3077_07_2218_tensor",
        }
    )
)

khat_source_rows = [
    base(
        {
            "source_audit_id": f"KHS3077_{index}_{spec['component']}",
            "component": spec["component"],
            "required_source": spec["khat_required"],
            "source_search_result": "NO_LIVE_COMPONENT_SOURCE_FOUND",
            "component_source_signed": "false",
            "fallback": "carry explicit DeltaK residual; do not set component to zero",
            "missing_for_claim": "MISSING_SOURCE_PATH_WITH_COMPONENT_FORMULA",
            "source_ids": spec["source_ids"],
        }
    )
    for index, spec in enumerate(component_specs)
]
khat_source_rows.append(
    base(
        {
            "source_audit_id": "KHS3077_7_verdict",
            "component": "live_Khat_tensor",
            "required_source": "one same-branch source defining all K_hat components used by q_loc",
            "source_search_result": "NO_LIVE_TENSOR_SOURCE_FOUND",
            "component_source_signed": "false",
            "fallback": "Delta_K cannot be killed; P4/source-bound route stays open",
            "missing_for_claim": "MISSING_LIVE_KHAT_TENSOR_DEFINITION",
            "source_ids": "SRC3077_06_2809_components;SRC3077_07_2218_tensor",
        }
    )
)

kmetric_requirement_rows = [
    base(
        {
            "requirement_id": f"KMRQ3077_{index}_{spec['component']}",
            "component": spec["component"],
            "required_kmetric_object": spec["kmetric_required"],
            "current_status": "FORMAL_DEFINITION_ONLY_VALUE_MISSING",
            "component_value_present": "false",
            "component_match_signed": "false",
            "missing_for_claim": "MISSING_GAMMA_EFF_DENSITY;MISSING_METRIC_VARIATION_VALUE;MISSING_BOUNDARY_DOMAIN_TERMS",
            "source_ids": spec["source_ids"],
        }
    )
    for index, spec in enumerate(component_specs)
]
kmetric_requirement_rows.append(
    base(
        {
            "requirement_id": "KMRQ3077_7_verdict",
            "component": "K_metric_total",
            "required_kmetric_object": "complete Hilbert response of a source-signed Gamma_eff density",
            "current_status": "FORMAL_DEFINITION_ONLY_NO_LIVE_VALUES",
            "component_value_present": "false",
            "component_match_signed": "false",
            "missing_for_claim": "MISSING_GAMMA_EFF_PARENT_DENSITY;MISSING_KMETRIC_COMPONENT_VALUES",
            "source_ids": "SRC3077_04_3076_gamma;SRC3077_08_2409_match;SRC3077_09_2975_certificate",
        }
    )
)

helmholtz_rows = [
    base(
        {
            "gate_id": "HELM3077_0_input_tensor",
            "clause": "sourced T_GK tensor",
            "mathematical_test": "T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_hat^{mu nu} has sourced components",
            "current_status": "KHAT_COMPONENTS_MISSING",
            "helmholtz_evaluable": "false",
            "helmholtz_pass": "false",
            "implication_if_fail": "cannot test whether K_hat is variational",
            "next_action": "source K_hat components or keep Delta_K/H_GK rows",
            "source_ids": "SRC3077_11_2218_helmholtz",
        }
    ),
    base(
        {
            "gate_id": "HELM3077_1_second_variation",
            "clause": "variational stress integrability",
            "mathematical_test": "delta(sqrt(-g)T_GK^{mu nu})/delta g_{alpha beta} symmetric under exchange of metric variations up to boundary terms",
            "current_status": "NOT_EVALUABLE_WITHOUT_COMPONENTS",
            "helmholtz_evaluable": "false",
            "helmholtz_pass": "false",
            "implication_if_fail": "term shapes cannot be promoted to parent action",
            "next_action": "wait for component birth certificate",
            "source_ids": "SRC3077_11_2218_helmholtz;SRC3077_09_2975_certificate",
        }
    ),
    base(
        {
            "gate_id": "HELM3077_2_boundary_symmetry",
            "clause": "boundary and improvement symmetry",
            "mathematical_test": "boundary terms from two metric variations commute or reduce to allowed exact/no-flux terms",
            "current_status": "BOUNDARY_OPEN",
            "helmholtz_evaluable": "false",
            "helmholtz_pass": "false",
            "implication_if_fail": "boundary can obstruct local no-force claim",
            "next_action": "derive boundary primitive or finite edge coefficient rows",
            "source_ids": "SRC3077_11_2218_helmholtz;SRC3077_12_1289_derivative",
        }
    ),
    base(
        {
            "gate_id": "HELM3077_3_verdict",
            "clause": "Helmholtz verdict",
            "mathematical_test": "all Helmholtz clauses evaluable and pass",
            "current_status": "HELMHOLTZ_NOT_EVALUABLE_YET",
            "helmholtz_evaluable": "false",
            "helmholtz_pass": "false",
            "implication_if_fail": "H_GK remains official obstruction",
            "next_action": "do not claim parent action identity",
            "source_ids": "SRC3077_11_2218_helmholtz",
        }
    ),
]

p4_fill_rows = [
    base(
        {
            "p4_id": "P4F3077_0_TQ",
            "component": "K_P4_TQ",
            "theorem_zero_route": "prove metric/coframe-only local parent or algebraic connection equation forces torsion/nonmetricity zero",
            "numeric_source_route": "source c_T, T_bar, c_Q, Q_bar and weak-field observable map",
            "status": "FIRST_NEXT_TARGET_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_NO_INDEPENDENT_GAMMA_THEOREM;MISSING_C_T;MISSING_T_BAR;MISSING_C_Q;MISSING_Q_BAR",
            "source_ids": "SRC3077_05_3076_p4;SRC3077_14_3075_p4",
        }
    ),
    base(
        {
            "p4_id": "P4F3077_1_spin",
            "component": "K_P4_spin",
            "theorem_zero_route": "prove no independent spin-torsion current in the local matter/readout branch",
            "numeric_source_route": "source c_spin and S_axial_bar",
            "status": "QUEUE_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_NO_HYPERMOMENTUM_THEOREM;MISSING_C_SPIN;MISSING_S_AXIAL_BAR",
            "source_ids": "SRC3077_05_3076_p4;SRC3077_14_3075_p4",
        }
    ),
    base(
        {
            "p4_id": "P4F3077_2_projective",
            "component": "K_P4_proj",
            "theorem_zero_route": "prove projective invariance/silence in the observed local branch",
            "numeric_source_route": "source c_proj and P_projective_bar",
            "status": "QUEUE_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_PROJECTIVE_INVARIANCE;MISSING_C_PROJ;MISSING_P_PROJECTIVE_BAR",
            "source_ids": "SRC3077_05_3076_p4;SRC3077_14_3075_p4",
        }
    ),
    base(
        {
            "p4_id": "P4F3077_3_QW",
            "component": "K_P4_QW",
            "theorem_zero_route": "prove Weyl nonmetricity is absent from local rods/clocks",
            "numeric_source_route": "source c_QW, Q_W_bar and clock/rod map",
            "status": "QUEUE_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_C_QW;MISSING_Q_W_BAR;MISSING_CLOCK_ROD_MAP",
            "source_ids": "SRC3077_05_3076_p4;SRC3077_14_3075_p4",
        }
    ),
    base(
        {
            "p4_id": "P4F3077_4_QTF",
            "component": "K_P4_QTF",
            "theorem_zero_route": "prove tracefree nonmetricity is absent from local lightcone/shear response",
            "numeric_source_route": "source c_QTF, Q_TF_bar and lightcone map",
            "status": "QUEUE_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_C_QTF;MISSING_Q_TF_BAR;MISSING_LIGHTCONE_MAP",
            "source_ids": "SRC3077_05_3076_p4;SRC3077_14_3075_p4",
        }
    ),
    base(
        {
            "p4_id": "P4F3077_5_H",
            "component": "K_P4_H",
            "theorem_zero_route": "prove no hypermomentum/source/readout connection current",
            "numeric_source_route": "source c_H and H_bar",
            "status": "QUEUE_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_NO_HYPERMOMENTUM_THEOREM;MISSING_C_H;MISSING_H_BAR",
            "source_ids": "SRC3077_05_3076_p4;SRC3077_14_3075_p4",
        }
    ),
    base(
        {
            "p4_id": "P4F3077_6_total",
            "component": "K_P4_bar",
            "theorem_zero_route": "all P4 theorem-zero routes close",
            "numeric_source_route": "all P4 component bounds have common units and arena projections",
            "status": "TOTAL_QUEUE_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_ALL_COMPONENT_THEOREM_ZERO_OR_NUMERIC_BOUNDS",
            "source_ids": "SRC3077_05_3076_p4;SRC3077_14_3075_p4",
        }
    ),
]

local_blocker_rows = [
    base(
        {
            "arena_id": "LBA3077_0_local_GR_Newton",
            "arena": "local GR/Newton",
            "required_before_pass": "Delta_K theorem-zero/bound plus P4/P_loc/domain/boundary/units closure",
            "current_blocker": "Delta_K components not born; Khat source missing",
            "arena_pass": "false",
            "local_gr_claim": "false",
            "next_evidence_needed": "DeltaK component birth certificate or explicit residual bound vector",
        }
    ),
    base(
        {
            "arena_id": "LBA3077_1_PPN",
            "arena": "PPN",
            "required_before_pass": "00,0i,trace,tracefree and preferred-frame residuals bounded against PPN tolerances",
            "current_blocker": "component rows missing formulas and units",
            "arena_pass": "false",
            "local_gr_claim": "false",
            "next_evidence_needed": "component-to-PPN response map",
        }
    ),
    base(
        {
            "arena_id": "LBA3077_2_R10",
            "arena": "R10 short-range",
            "required_before_pass": "DeltaK_00/trace and P4 TQ/QW/QTF residuals bounded with length scale and alpha(lambda) map",
            "current_blocker": "no component amplitude or units",
            "arena_pass": "false",
            "local_gr_claim": "false",
            "next_evidence_needed": "source-backed local residual amplitude rows",
        }
    ),
    base(
        {
            "arena_id": "LBA3077_3_clocks_WEP_orbits",
            "arena": "clocks/WEP/orbital",
            "required_before_pass": "clock/rod/projector/domain maps and spin/nonmetricity/hypermomentum residual bounds",
            "current_blocker": "P4 and projector/domain queues are nonclaim",
            "arena_pass": "false",
            "local_gr_claim": "false",
            "next_evidence_needed": "P4 first-component source/theorem-zero rows",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3077_0_birth_certificate",
            "decision": "Delta_K component birth certificate not signed",
            "reason": "no live K_hat component source and no live K_metric component values exist for 00, 0i, trace, tracefree, derivative/boundary, units or projector/domain",
            "consequence": "Delta_K remains an explicit obstruction",
            "next_action": "do not claim q_loc zero or local GR",
        }
    ),
    base(
        {
            "decision_id": "DEC3077_1_helmholtz",
            "decision": "Helmholtz test remains not evaluable",
            "reason": "the tensor input and boundary convention required for second-variation symmetry are missing",
            "consequence": "K_hat cannot be promoted to a parent action response",
            "next_action": "wait for sourced tensor components or keep H_GK obstruction",
        }
    ),
    base(
        {
            "decision_id": "DEC3077_2_P4_start",
            "decision": "P4 source/theorem-zero queue opened",
            "reason": "after the component certificate fails, the official fallback is to source or theorem-zero P4 components",
            "consequence": "first attack should be K_P4_TQ because torsion/nonmetricity is the broadest connection residue",
            "next_action": "3078-Y5-R2FR-P4-TQ-first-source-or-theorem-zero-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3077_0_DeltaK_zero",
            "claim": "Delta_K is zero or bounded enough for local GR",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "component birth certificates are unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3077_1_Khat_components",
            "claim": "live K_hat components are sourced",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "component source audit found no live component formulas",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3077_2_Helmholtz",
            "claim": "K_hat is a variational parent-action response",
            "claim_active": "false",
            "status": "NOT_EVALUABLE",
            "reason": "missing components and boundary convention block Helmholtz test",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3077_3_local_arenas",
            "claim": "local GR/Newton/PPN/R10/clock/WEP/orbital arenas pass",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "Delta_K and P4 queues remain nonclaim",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3077_0_3078",
            "next_checkpoint": "3078-Y5-R2FR-P4-TQ-first-source-or-theorem-zero-under-AX1090.md",
            "script": "scripts/Y5_R2FR_P4_TQ_first_source_or_theorem_zero_under_AX1090_3078.py",
            "mission": "attack K_P4_TQ first: prove torsion/nonmetricity silence from the local geometry grammar, or create source-backed c_T,T_bar,c_Q,Q_bar rows with units and arena projections",
            "starting_equation": "K_P4_TQ <= c_T T_bar + c_Q Q_bar; K_conn_bar <= K_LC_stack_bar + K_P4_bar",
            "claim_policy": "no local-GR/PPN/R10 claim unless P4_TQ is theorem-zero or numerically bounded and Delta_K/P_loc/domain/boundary queues remain explicit",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["birth_certificate"], birth_certificate_rows)
write_csv(OUTPUTS["khat_source"], khat_source_rows)
write_csv(OUTPUTS["kmetric_requirements"], kmetric_requirement_rows)
write_csv(OUTPUTS["helmholtz"], helmholtz_rows)
write_csv(OUTPUTS["p4_fill"], p4_fill_rows)
write_csv(OUTPUTS["local_blockers"], local_blocker_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["birth_certificate"], BRANCH_OUTPUTS["birth_certificate_copy"])
copy_csv(OUTPUTS["khat_source"], BRANCH_OUTPUTS["khat_source_copy"])
copy_csv(OUTPUTS["local_blockers"], BRANCH_OUTPUTS["local_blockers_copy"])
copy_csv(OUTPUTS["p4_fill"], BRANCH_OUTPUTS["p4_fill_copy"])
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
        ("BC3077_0_birth_certificate", OUTPUTS["birth_certificate"], BRANCH_OUTPUTS["birth_certificate_copy"]),
        ("BC3077_1_khat_source", OUTPUTS["khat_source"], BRANCH_OUTPUTS["khat_source_copy"]),
        ("BC3077_2_local_blockers", OUTPUTS["local_blockers"], BRANCH_OUTPUTS["local_blockers_copy"]),
        ("BC3077_3_p4_fill", OUTPUTS["p4_fill"], BRANCH_OUTPUTS["p4_fill_copy"]),
        ("BC3077_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)
write_csv(
    OUTPUTS["validation"],
    [
        base(
            {
                "validation_id": "VAL3077_PRE",
                "passed": "False",
                "requirement": "placeholder overwritten by final validation",
                "evidence": "generator ordering guard",
            }
        )
    ],
)
DOC.write_text("# 3077 draft\n", encoding="utf-8")

remove_pycache()
dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
generated_rows = (
    birth_certificate_rows
    + khat_source_rows
    + kmetric_requirement_rows
    + helmholtz_rows
    + p4_fill_rows
    + local_blocker_rows
    + decision_rows
    + claim_rows
    + next_rows
)
formalization_output_count = sum(1 for output_path in generated_csvs + [DOC] if under(output_path, FORMALIZATION))
required_components = {
    "DeltaK_00",
    "DeltaK_0i",
    "DeltaK_trace",
    "DeltaK_TF",
    "DeltaK_derivative_boundary",
    "DeltaK_units",
    "DeltaK_projector_domain",
    "Delta_K_total",
}
birth_components = {row["component"] for row in birth_certificate_rows}
p4_components = {row["component"] for row in p4_fill_rows}

validation_rows = [
    base(
        {
            "validation_id": "VAL3077_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3077_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3077_02_csv_parse",
            "passed": str(all(csv_ok(output_path) for output_path in generated_csvs)),
            "requirement": "all generated and branch-copy CSVs parse cleanly",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3077_03_birth_certificate_not_signed",
            "passed": str(not any(boolish(row["certificate_signed"]) or boolish(row["component_match_signed"]) for row in birth_certificate_rows)),
            "requirement": "Delta_K component birth certificates remain unsigned",
            "evidence": OUTPUTS["birth_certificate"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3077_04_components_complete",
            "passed": str(required_components.issubset(birth_components)),
            "requirement": "Delta_K birth-certificate vector includes total, 00, 0i, trace, tracefree, derivative/boundary, units and projector/domain",
            "evidence": OUTPUTS["birth_certificate"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3077_05_khat_sources_missing",
            "passed": str(not any(boolish(row["component_source_signed"]) for row in khat_source_rows)),
            "requirement": "live K_hat component sources remain missing rather than fabricated",
            "evidence": OUTPUTS["khat_source"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3077_06_kmetric_values_missing",
            "passed": str(not any(boolish(row["component_value_present"]) or boolish(row["component_match_signed"]) for row in kmetric_requirement_rows)),
            "requirement": "K_metric component values are not treated as present",
            "evidence": OUTPUTS["kmetric_requirements"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3077_07_helmholtz_not_evaluable",
            "passed": str(not any(boolish(row["helmholtz_evaluable"]) or boolish(row["helmholtz_pass"]) for row in helmholtz_rows)),
            "requirement": "Helmholtz gate remains not evaluable without sourced tensor components",
            "evidence": OUTPUTS["helmholtz"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3077_08_P4_queue_complete_nonclaim",
            "passed": str({"K_P4_TQ", "K_P4_spin", "K_P4_proj", "K_P4_QW", "K_P4_QTF", "K_P4_H", "K_P4_bar"}.issubset(p4_components) and not has_claim_true(p4_fill_rows)),
            "requirement": "P4 source/theorem-zero queue is complete and nonclaim",
            "evidence": OUTPUTS["p4_fill"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3077_09_local_arenas_blocked",
            "passed": str(not any(boolish(row["arena_pass"]) or boolish(row["local_gr_claim"]) for row in local_blocker_rows)),
            "requirement": "all local arenas remain blocked if Delta_K/P4 evidence is missing",
            "evidence": OUTPUTS["local_blockers"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3077_10_no_claim_promoted",
            "passed": str(not has_claim_true(claim_rows + decision_rows + local_blocker_rows)),
            "requirement": "no q_loc zero, local-GR, PPN, R10, clock, WEP or orbital claim is promoted",
            "evidence": OUTPUTS["claim_status"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3077_11_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3078-Y5-R2FR-P4-TQ")),
            "requirement": "next target moves to P4_TQ first source or theorem-zero",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3077_12_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3077_13_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3077_14_outputs_under_post_checkpoint",
            "passed": str(all(under(output_path, ROOT) for output_path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3077_15_no_formalization_outputs",
            "passed": str(formalization_output_count == 0),
            "requirement": "formalization-workbench modified-file count for 3077 outputs remains zero",
            "evidence": f"formalization_3077_output_paths={formalization_output_count}",
        }
    ),
    base(
        {
            "validation_id": "VAL3077_16_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3077_17_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
    base(
        {
            "validation_id": "VAL3077_18_no_claim_fields_true",
            "passed": str(not has_claim_true(generated_rows)),
            "requirement": "no generated non-validation row contains a true claim/ready field",
            "evidence": "claim field scan",
        }
    ),
]

write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3077 - DeltaK Component Birth Certificate or P4 Numeric Source Fill

Status: `Y5_R2FR_3077_DeltaK_birth_certificate_not_signed_P4_TQ_next`

Generated: `{RUN_UTC}`

## Verdict

3077 tried the component-level route: turn the `Delta_K` obstruction from 3076 into a birth certificate for the live `K_hat` tensor against `K_metric[Gamma_eff]`.

This does **not** close. The formal definition of `K_metric` exists, but the current corpus still has no live source-signed `K_hat` component formulas for `00`, `0i`, spatial trace, spatial tracefree, derivative/boundary, units, or projector/domain order. Because those inputs are absent, the Helmholtz/integrability test is still not evaluable.

So 3077 does **not** claim `Delta_K=0`, `K_hat=K_metric[Gamma_eff]`, `q_loc=0`, local GR, Newtonian recovery, PPN, R10, clocks, WEP, or orbital success.

The useful leap is that the failure is now operational: each component has a required birth certificate. Since the certificate cannot be signed from current sources, the next clean route is to start the official P4 fallback with the broadest residue, `K_P4_TQ`.

## DeltaK Birth-Certificate Audit

{md_table(birth_certificate_rows, ["certificate_id", "component", "certificate_status", "certificate_signed", "current_evidence"])}

## Khat Live Component Source Audit

{md_table(khat_source_rows, ["source_audit_id", "component", "source_search_result", "component_source_signed", "fallback"])}

## Kmetric Component Requirement Ledger

{md_table(kmetric_requirement_rows, ["requirement_id", "component", "current_status", "component_value_present", "missing_for_claim"])}

## Helmholtz Evaluable Gate

{md_table(helmholtz_rows, ["gate_id", "clause", "current_status", "helmholtz_evaluable", "helmholtz_pass"])}

## P4 Source/Theorem-Zero Queue

{md_table(p4_fill_rows, ["p4_id", "component", "status", "theorem_zero_route", "numeric_source_route"])}

## Local Arena Blockers

{md_table(local_blocker_rows, ["arena_id", "arena", "current_blocker", "arena_pass", "next_evidence_needed"])}

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
- DeltaK birth certificate audit: `{OUTPUTS["birth_certificate"]}`
- Khat live component source audit: `{OUTPUTS["khat_source"]}`
- Kmetric requirement ledger: `{OUTPUTS["kmetric_requirements"]}`
- Helmholtz gate: `{OUTPUTS["helmholtz"]}`
- P4 source/theorem-zero queue: `{OUTPUTS["p4_fill"]}`
- Local arena blockers: `{OUTPUTS["local_blockers"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
- Branch copy: `{BRANCH_OUTPUTS["birth_certificate_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["khat_source_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["local_blockers_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["p4_fill_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["next_copy"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
print(f"Wrote {DOC}")
print(f"Wrote {OUTPUTS['validation']}")
print(f"Validation passed {sum(1 for row in validation_rows if row['passed'] == 'True')}/{len(validation_rows)}")
