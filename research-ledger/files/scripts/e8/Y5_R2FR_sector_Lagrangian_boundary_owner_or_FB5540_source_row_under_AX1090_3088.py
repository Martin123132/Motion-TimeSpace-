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
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3088"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3088-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3088_00_3087_doc": {
        "path": ROOT / "3087-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds-under-AX1090.md",
        "needles": ["source-charge owner problem", "M_H_ref"],
        "role": "3087 narrows the residual-sector problem to source-charge ownership.",
    },
    "SRC3088_01_3087_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3087_NEXT_TARGET.csv",
        "needles": ["NEXT3087_0_3088", "FB5540-source-row"],
        "role": "3087 handoff names this sector owner / FB5540 source-row target.",
    },
    "SRC3088_02_3087_bound_pack": {
        "path": RESIDUALS / "P8_Y5_R2FR_3087_OPERATOR_BOUND_INPUT_PACK_NONCLAIM.csv",
        "needles": ["OBI3087_6_source_normalization", "MISSING_MHREF_AND_FB5540_COMPONENTS"],
        "role": "3087 identifies M_H_ref and FB5540 numerator components as the root operator-bound row.",
    },
    "SRC3088_03_1842_precedent": {
        "path": ROOT / "1842-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
        "needles": ["OWNER_MAP_SHARP_BUT_NOT_CLOSED", "FULL_NO_CANCELLATION_SOURCE_ROW_REQUIRED_IF_THEOREM_FAILS"],
        "role": "1842 precedent supplies the owner-map fork and source-row fallback.",
    },
    "SRC3088_04_1017_hamiltonian_lock": {
        "path": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "needles": ["FB554_0", "M_H_ref"],
        "role": "1017 splits FB5540 into integrability, reference, boundary, tau and M_H_ref clauses.",
    },
    "SRC3088_05_1018_owner_map": {
        "path": ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
        "needles": ["sector-owner map", "no theorem-zero route"],
        "role": "1018 gives the modern sector-owner map and source-row schema.",
    },
    "SRC3088_06_1018_schema": {
        "path": RESIDUALS / "P8_Y5_R10_1018_SOURCE_ROW_SCHEMA.csv",
        "needles": ["FSR1018_0_M_H_ref", "NOT_COMPUTED_COMPONENTS_MISSING"],
        "role": "1018 source schema lists the M_H_ref, bulk, edge and total guard inputs.",
    },
    "SRC3088_07_1019_boundary_projector": {
        "path": ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["edge/boundary obstruction", "neither is parent-signed"],
        "role": "1019 shows the boundary exactness/projector routes are precise but not signed.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3088_SOURCE_REGISTER.csv",
    "parent_contract": RESIDUALS / "P8_Y5_R2FR_3088_PARENT_ACTION_CONTRACT.csv",
    "owner_clauses": RESIDUALS / "P8_Y5_R2FR_3088_OWNER_CLAUSES.csv",
    "route_tests": RESIDUALS / "P8_Y5_R2FR_3088_THEOREM_ROUTE_TESTS.csv",
    "source_schema": RESIDUALS / "P8_Y5_R2FR_3088_FB5540_SOURCE_ROW_SCHEMA.csv",
    "source_runner": RESIDUALS / "P8_Y5_R2FR_3088_FB5540_SOURCE_ROW_RUNNER.csv",
    "guard": RESIDUALS / "P8_Y5_R2FR_3088_NO_CANCELLATION_GUARD.csv",
    "bridge": RESIDUALS / "P8_Y5_R2FR_3088_GR_BRIDGE_STATUS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3088_CLAIM_GATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3088_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3088_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3088_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3088_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "owner_clauses_copy": LOCAL_BOUNDS / "sector_Lagrangian_boundary_owner_3088_NONCLAIM.csv",
    "source_schema_copy": LOCAL_BOUNDS / "FB5540_source_row_schema_3088_NONCLAIM.csv",
    "guard_copy": LOCAL_BOUNDS / "no_cancellation_guard_3088_NONCLAIM.csv",
    "bridge_copy": LOCAL_BOUNDS / "GR_bridge_status_3088_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3088_boundary_exactness_projector_or_FB5540_source_pack_NEXT_NONCLAIM.csv",
}


def metadata() -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


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


def with_meta(output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base = metadata()
    return [{**base, **output_row} for output_row in output_rows]


def source_register_rows() -> list[dict[str, Any]]:
    output_rows: list[dict[str, Any]] = []
    for source_id, source in SOURCE_PATHS.items():
        path = Path(source["path"])
        content = text(path)
        missing = [needle for needle in source["needles"] if needle not in content]
        output_rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "parse_ok": source_parse_ok(path),
                "sha256": file_hash(path),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return with_meta(output_rows)


def parent_contract_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "contract_id": "PAC3088_0_action_split",
                "required_clause": "single parent action splits EH plus explicit extra-sector Lagrangians",
                "mathematical_form": "S_parent=S_EH[g]+sum_X int_M L_X[g,X,nabla X]+int_partialM B_parent",
                "why_needed": "sector variation is otherwise notation rather than derivation",
                "current_status": "FORM_REQUIRED_NOT_PARENT_SIGNED",
                "blocks": "EH_dominance;Newton_GR;PPN_R10_clock_orbit_scoring",
                "next_action": "derive exact L_X from parent variables or retain source-backed coefficient row",
            },
            {
                "contract_id": "PAC3088_1_variation_charge",
                "required_clause": "sector variation owns symplectic potential and Hamiltonian charge",
                "mathematical_form": "delta L_X=E_X delta X+dTheta_X; J_tau^X=Theta_X(L_tau X)-i_tau L_X=dQ_tau^X+C_tau^X",
                "why_needed": "FB5540 numerator terms are Hamiltonian/symplectic objects",
                "current_status": "FORMULA_WRITTEN_OWNER_UNSIGNED",
                "blocks": "delta_H_tau_nonintegrable;symplectic_boundary_flux;Q_edge",
                "next_action": "derive Theta_X,Q_tau^X and constraint current from the same parent action",
            },
            {
                "contract_id": "PAC3088_2_quotient_vertical",
                "required_clause": "extra-sector direction is either physical with sourced coefficients or vertical first-class",
                "mathematical_form": "either qbar_X != 0 with sourced K_X,Qbar_XH,qbar_XT or Dq[v_X]=0 and delta G_X=Omega(delta Phi,v_X)",
                "why_needed": "prevents smuggling a local plateau by declaring X unobservable after the fact",
                "current_status": "ROUTE_SPLIT_WRITTEN_NOT_SIGNED",
                "blocks": "K_X;Qbar_XH;qbar_XT;projector_orthogonality",
                "next_action": "prove vertical first-class with zero differentiable boundary charge or source the physical residual",
            },
            {
                "contract_id": "PAC3088_3_boundary_reference",
                "required_clause": "reference subtraction and boundary class are selected before readout",
                "mathematical_form": "B_ref[gamma_ref,tau_ref,C_top] with partial_{source,r,t,frame,lambda}Delta_ref=0",
                "why_needed": "otherwise source normalization can be fitted by reference choice",
                "current_status": "NOT_SIGNED",
                "blocks": "Delta_ref;Delta_symp;B_zero_flux",
                "next_action": "derive B_ref and boundary class/no-hair condition from parent variational principle",
            },
            {
                "contract_id": "PAC3088_4_tau_lock",
                "required_clause": "same generator controls source charge, clocks, PPN and readout",
                "mathematical_form": "tau_source=tau_charge=tau_clock=tau_readout up to source-backed mismatch bound",
                "why_needed": "M_H_ref must be the same object used by orbital and local tests",
                "current_status": "NOT_SIGNED",
                "blocks": "tau_lock_mismatch;clock_branch;PPN_branch",
                "next_action": "derive tau from the parent foliation/observer prescription or carry tau mismatch as a bound row",
            },
            {
                "contract_id": "PAC3088_5_MHref_positive",
                "required_clause": "same-frame Hamiltonian/Hilbert source denominator exists before empirical readout",
                "mathematical_form": "M_H_ref=H_tau[S_outer]-H_ref=int_S(Q_tau-i_tau B)-H_ref > 0",
                "why_needed": "FB5540 and projector residuals need a non-circular denominator",
                "current_status": "MISSING_STABLE_MH_REF",
                "blocks": "source_normalization;Newton_Poisson;local_GR",
                "next_action": "derive positivity and frame lock or fill first source-backed M_H_ref row",
            },
            {
                "contract_id": "PAC3088_6_zero_or_source_pack",
                "required_clause": "every residual is theorem-zero or source-backed with no-cancellation guard",
                "mathematical_form": "epsilon_source <= (|R_eq|+|B_zero|+|I_commutator|+|Delta_ref|+|Delta_symp|+|delta_H_tau|)/M_H_ref",
                "why_needed": "unknown residuals cannot be cancelled symbolically",
                "current_status": "CONTRACT_WRITTEN_CURRENTLY_UNSATISFIED",
                "blocks": "claim_ready_residual_vector",
                "next_action": "prove boundary/projector zeros or complete FB5540 source pack",
            },
            {
                "contract_id": "PAC3088_7_verdict",
                "required_clause": "parent action contract closes current MTS local branch",
                "mathematical_form": "PAC3088_0 through PAC3088_6 all parent-signed together",
                "why_needed": "this is the minimum route to a derivable GR/Newton source normalization",
                "current_status": "FAIL_CURRENT_CLAIM",
                "blocks": "Newton_GR_claim;PPN_R10_clock_orbit_claim",
                "next_action": "move to boundary exactness/projector orthogonality or FB5540 source-pack construction",
            },
        ]
    )


def owner_clause_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "owner_id": "LOC3088_0_LX_owner",
                "required_owner": "parent-owned extra-sector Lagrangian",
                "mathematical_form": "L_X[g,X,nabla X] with explicit operator, source term, normalization and boundary conditions",
                "current_status": "NOT_SIGNED",
                "failure_if_missing": "Theta_X,Q_X,omega_X,C_X,R10/R11 and local scaling cannot be computed",
                "feeds": "delta_H_tau_nonintegrable_over_MH;C_extra;R10;R11",
            },
            {
                "owner_id": "LOC3088_1_Theta_QX_owner",
                "required_owner": "sector symplectic potential and Hamiltonian charge",
                "mathematical_form": "delta L_X=E_X delta X+dTheta_X; J_tau^X=Theta_X(L_tau X)-i_tau L_X=dQ_tau^X+C_tau^X",
                "current_status": "FORMULA_WRITTEN_NOT_OWNED",
                "failure_if_missing": "Hamiltonian integrability remains schematic",
                "feeds": "delta_H_tau_nonintegrable_over_MH;symplectic_boundary_flux_over_MH",
            },
            {
                "owner_id": "LOC3088_2_no_pole_quotient",
                "required_owner": "X is absent from physical quotient or first-class vertical",
                "mathematical_form": "Dq[v_X]=0 and delta G_X=Omega(delta Phi,v_X) differentiable with zero boundary charge",
                "current_status": "CONDITIONAL_ROUTE_UNSIGNED",
                "failure_if_missing": "parent Omega/DC_X and boundary charge owner do not close",
                "feeds": "K_X;qbar_XT;Qbar_XH",
            },
            {
                "owner_id": "LOC3088_3_positive_sourcefree",
                "required_owner": "positive source-free local X operator",
                "mathematical_form": "O_X X=-nabla_i(Z_X nabla^i X)+M_X^2 X with Z_X>0,M_X^2>0,J_X=0,boundary_flux_X=0",
                "current_status": "CONDITIONAL_THEOREM_UNSIGNED",
                "failure_if_missing": "Z_X,M_X^2,J_X=0 and boundary_flux_X=0 are not parent-signed together",
                "feeds": "lambda_X;alpha_X;R10;R11",
            },
            {
                "owner_id": "LOC3088_4_Bref_owner",
                "required_owner": "reference boundary functional selected before readout",
                "mathematical_form": "B_ref[gamma_ref,tau_ref,C_top] with partial_{source,r,t,frame,lambda}Delta_ref=0",
                "current_status": "NOT_SIGNED",
                "failure_if_missing": "reference can absorb source calibration",
                "feeds": "Delta_ref_over_MH;Delta_symp_over_MH",
            },
            {
                "owner_id": "LOC3088_5_Bclass_owner",
                "required_owner": "boundary class/no-hair/projector silence",
                "mathematical_form": "B_class[chi_B,C_top] plus exact/proper-gauge/no-vector-tensor-hair conditions",
                "current_status": "NOT_SIGNED",
                "failure_if_missing": "symplectic boundary flux and edge charge remain live",
                "feeds": "B_zero_flux;symplectic_boundary_flux;Qbar_edge_XH",
            },
            {
                "owner_id": "LOC3088_6_tau_owner",
                "required_owner": "same generator for source, charge, clocks and readout",
                "mathematical_form": "tau_source=tau_charge=tau_clock=tau_readout up to source-backed mismatch bound",
                "current_status": "NOT_SIGNED",
                "failure_if_missing": "Hamiltonian source charge and clock/PPN readout can drift apart",
                "feeds": "tau_lock_mismatch;clock;PPN;M_H_ref",
            },
            {
                "owner_id": "LOC3088_7_MHref_owner",
                "required_owner": "same-frame Hamiltonian/Hilbert source denominator",
                "mathematical_form": "M_H_ref=H_tau[S_outer]-H_ref=int_S(Q_tau-i_tau B)-H_ref, positive and fixed before orbital readout",
                "current_status": "MISSING_STABLE_MH_REF",
                "failure_if_missing": "R_eq/FB5540/source-normalization rows are unnormalized",
                "feeds": "FB5540;R_eq;I_commutator;Newton;local_GR",
            },
            {
                "owner_id": "LOC3088_8_verdict",
                "required_owner": "all owners needed for FB5540 and local-GR source charge",
                "mathematical_form": "LOC3088_0 through LOC3088_7 parent-signed together",
                "current_status": "FAIL_CURRENT_CLAIM",
                "failure_if_missing": "current MTS has an explicit owner map but not owner closure",
                "feeds": "FB5540;R10;R11;local_GR",
            },
        ]
    )


def route_test_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "route_id": "RT3088_0_direct_parent_owner",
                "route": "derive full L_X/Theta_X/Q_X/B/tau/M_H_ref owner from one parent action",
                "mathematical_test": "one parent variational principle supplies E_X,Theta_X,Q_X,B_ref,B_class,tau,M_H_ref before readout",
                "current_status": "BEST_ROUTE_UNSIGNED",
                "if_success": "FB5540 terms become computable or theorem-zero in the same frame",
                "blocker": "sector Lagrangian and boundary/tau owners are incomplete",
                "fallback": "FB5540 source-row pack",
            },
            {
                "route_id": "RT3088_1_vertical_first_class_zero",
                "route": "X is vertical first-class and carries no boundary charge",
                "mathematical_test": "Dq[v_X]=0; delta G_X=Omega(delta Phi,v_X); Q_tau^X|partialA=0; K_X=Qbar_XH=qbar_XT=0",
                "current_status": "ZERO_ROUTE_NOT_SIGNED",
                "if_success": "bulk X exchange residual is killed without fitting alpha",
                "blocker": "differentiable generator and zero boundary charge are not parent-signed",
                "fallback": "bulk coefficient row for K_X,Qbar_XH,qbar_XT",
            },
            {
                "route_id": "RT3088_2_positive_sourcefree_zero",
                "route": "positive source-free local operator kills local X profile",
                "mathematical_test": "int_A(Z_X|grad X|^2+M_X^2 X^2)=int_A XJ_X+int_partialA X n.Z_X gradX; RHS=0",
                "current_status": "CONDITIONAL_THEOREM_ONLY",
                "if_success": "X=0 in local exterior and alpha_X=0",
                "blocker": "Z_X>0,M_X^2>0,J_X=0 and boundary flux zero are not signed together",
                "fallback": "lambda_X and alpha_X source row",
            },
            {
                "route_id": "RT3088_3_boundary_exact_projector_zero",
                "route": "edge boundary form is exact or projected orthogonal",
                "mathematical_test": "Q_edge=deta on compact linked surface or Pi_M^H[Q_edge]=0 with no double count against bulk X",
                "current_status": "PRECISE_BUT_PARENT_UNSIGNED",
                "if_success": "Qbar_edge_XH and K_boundary vanish before scoring",
                "blocker": "boundary class, projector domain and cocycle/no-double-count clauses are not signed",
                "fallback": "edge residual coefficient pack",
            },
            {
                "route_id": "RT3088_4_massive_sourced_residual",
                "route": "finite physical X residual",
                "mathematical_test": "lambda_X=sqrt(Z_X/M_X^2); alpha_X=K_X Qbar_XH qbar_XT with units and source paths",
                "current_status": "SCHEMA_READY_NO_VALUES",
                "if_success": "R10/R11 can score as a nonclaim empirical branch",
                "blocker": "all coefficients/units/source paths missing or nonclaim",
                "fallback": "source acquisition required",
            },
            {
                "route_id": "RT3088_5_FB5540_source_pack",
                "route": "complete no-cancellation source pack",
                "mathematical_test": "M_H_ref and every numerator component are theorem-zero or sourced, then abs-sum guard is computed",
                "current_status": "REQUIRED_IF_ZERO_ROUTES_FAIL",
                "if_success": "source-normalization row becomes score-ready without borrowing orbital GM",
                "blocker": "M_H_ref and numerator components missing",
                "fallback": "hold Newton/local-GR gates closed",
            },
            {
                "route_id": "RT3088_6_verdict",
                "route": "sector Lagrangian/boundary owner closes",
                "mathematical_test": "one zero-theorem route closes or source-backed rows exist with no-cancellation guard",
                "current_status": "FAIL_CURRENT_CLAIM",
                "if_success": "local GR gate can reopen",
                "blocker": "no route signs enough clauses or supplies source-backed values",
                "fallback": "boundary exactness/projector orthogonality or FB5540 source-pack checkpoint",
            },
        ]
    )


def source_schema_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "row_id": "FSR3088_0_M_H_ref",
                "quantity": "M_H_ref",
                "definition": "same-frame Hamiltonian source denominator",
                "required_columns": "system_id;surface;Q_tau_integral;B_integral;H_ref;M_H_ref;units;source_path;assumptions;valid_for_claim",
                "current_status": "MISSING_STABLE_MH_REF",
            },
            {
                "row_id": "FSR3088_1_delta_H_tau",
                "quantity": "delta_H_tau_nonintegrable_over_MH",
                "definition": "field-space curl of Hamiltonian variation normalized by M_H_ref",
                "required_columns": "system_id;surface_pair;omega_X_integral;reference_curl;M_H_ref;units;source_path;assumptions;valid_for_claim",
                "current_status": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            },
            {
                "row_id": "FSR3088_2_Delta_ref",
                "quantity": "Delta_ref_over_MH",
                "definition": "reference shift/derivative profile normalized by M_H_ref",
                "required_columns": "system_id;reference_branch;Delta_ref;derivative_profile;M_H_ref;units;source_path;assumptions;valid_for_claim",
                "current_status": "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            },
            {
                "row_id": "FSR3088_3_boundary_flux",
                "quantity": "symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp",
                "definition": "boundary/projector/non-EH linked flux normalized by M_H_ref",
                "required_columns": "system_id;surface_pair;symplectic_boundary_flux;B_zero_flux;Delta_symp;M_H_ref;units;source_path;assumptions;valid_for_claim",
                "current_status": "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
            },
            {
                "row_id": "FSR3088_4_LX_bulk_coefficients",
                "quantity": "Z_X;M_X2;J_X;lambda_X",
                "definition": "bulk X-sector coefficients if no theorem-zero route closes",
                "required_columns": "system_id;field_id;Z_X;M_X2;J_X;lambda_X;units;source_path;assumptions;valid_for_claim",
                "current_status": "MISSING_PARENT_INPUT",
            },
            {
                "row_id": "FSR3088_5_R10_source_projection",
                "quantity": "K_X;Qbar_XH;qbar_XT",
                "definition": "R10 residual amplitude factors for active X exchange",
                "required_columns": "system_id;K_X;Qbar_XH;qbar_XT;normalization;units;source_path;assumptions;valid_for_claim",
                "current_status": "MISSING_ARENA_PROJECTION",
            },
            {
                "row_id": "FSR3088_6_edge_projection",
                "quantity": "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT",
                "definition": "edge/boundary residual amplitude factors if boundary theorem fails",
                "required_columns": "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;units;source_path;assumptions;valid_for_claim",
                "current_status": "MISSING_EDGE_COEFFICIENTS",
            },
            {
                "row_id": "FSR3088_7_total_guard",
                "quantity": "FB5540_alpha_R11_total_guard",
                "definition": "no-cancellation envelope across FB5540, bulk X, edge X and R11 coefficients",
                "required_columns": "system_id;component_sum_abs;M_H_ref;normalization;source_path;assumptions;valid_for_claim",
                "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            },
        ]
    )


def source_runner_rows(schema: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output_rows: list[dict[str, Any]] = []
    for index, row in enumerate(schema):
        output_rows.append(
            {
                "runner_id": f"FRR3088_{index}_{row['row_id'].split('_', 2)[-1]}",
                "row_id": row["row_id"],
                "quantity": row["quantity"],
                "computed_status": "BLOCKED_MISSING_INPUTS",
                "claim_allowed": False,
                "failure_reasons": "MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE",
            }
        )
    return with_meta(output_rows)


def guard_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "guard_id": "NCG3088_0_unknown_cancellation_ban",
                "guard": "unknown residual components cannot be cancelled against each other",
                "required_test": "component_sum_abs is computed before signed total",
                "current_status": "ACTIVE_BAN",
                "claim_impact": "blocks any claim from symbolic cancellations",
            },
            {
                "guard_id": "NCG3088_1_denominator_ban",
                "guard": "orbital GM or fitted galaxy/cosmology amplitude cannot be used as M_H_ref",
                "required_test": "M_H_ref is parent/Hamiltonian sourced before readout",
                "current_status": "ACTIVE_BAN",
                "claim_impact": "blocks Newton/GR bridge unless source charge is independent",
            },
            {
                "guard_id": "NCG3088_2_zero_route_guard",
                "guard": "zero theorem must kill the component before empirical scoring",
                "required_test": "theorem-zero row cites parent action, boundary class and projection domain",
                "current_status": "ACTIVE_BAN",
                "claim_impact": "prevents closure-only local plateau claims",
            },
            {
                "guard_id": "NCG3088_3_source_pack_guard",
                "guard": "fallback row must include denominator and every numerator component",
                "required_test": "M_H_ref,R_eq,B_zero,I_commutator,Delta_ref,Delta_symp,delta_H_tau all sourced or theorem-zero",
                "current_status": "ACTIVE_BAN",
                "claim_impact": "keeps FB5540/source-normalization nonclaim until full pack exists",
            },
        ]
    )


def bridge_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "status_id": "GB3088_0_owner_contract",
                "bridge_piece": "parent-action owner contract",
                "current_status": "EXPLICIT_BUT_NOT_PARENT_SIGNED",
                "evidence": "PAC3088 and LOC3088 rows",
                "remaining_gap": "L_X,Theta_X,Q_X,B_ref,B_class,tau,M_H_ref not signed together",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3088_1_zero_routes",
                "bridge_piece": "vertical/source-free/boundary zero theorem routes",
                "current_status": "CONDITIONAL_NOT_PROMOTED",
                "evidence": "RT3088_1 through RT3088_3",
                "remaining_gap": "no route has parent-signed positivity, exactness, projector orthogonality and boundary charge zero",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3088_2_source_pack",
                "bridge_piece": "FB5540/source-normalization first row",
                "current_status": "SCHEMA_READY_NO_VALUES",
                "evidence": "FSR3088 and FRR3088 rows",
                "remaining_gap": "M_H_ref and numerator components missing",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3088_3_Newton_GR",
                "bridge_piece": "Newton/local-GR route",
                "current_status": "BLOCKED_AT_SOURCE_CHARGE",
                "evidence": "GB3088_0 through GB3088_2",
                "remaining_gap": "source normalization cannot be derived until zero theorem or no-cancellation source pack closes",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3088_4_empirical_route",
                "bridge_piece": "PPN/R10/clock/orbit residual scoring",
                "current_status": "NOT_SCORE_READY",
                "evidence": "FSR3088 schema rows",
                "remaining_gap": "source-backed numeric/theorem-zero rows absent",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3088_5_next",
                "bridge_piece": "next derivation owner",
                "current_status": "BOUNDARY_EXACTNESS_PROJECTOR_OR_FB5540_SOURCE_PACK_IS_NEXT",
                "evidence": "RT3088_3;RT3088_5;NCG3088",
                "remaining_gap": "prove Q_edge/projector zeros or build complete FB5540 source pack",
                "bridge_claim": False,
            },
        ]
    )


def gate_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "gate_id": "CG3088_0_contract_written",
                "claim": "minimal parent action contract has been written",
                "gate_pass": True,
                "reason": "PAC3088 specifies the exact clauses needed for a derivable source charge",
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3088_1_LX_owned",
                "claim": "L_X,Theta_X,Q_X,omega_X are parent-owned",
                "gate_pass": False,
                "reason": "candidate formulas are routes, not signed current-MTS derivations",
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3088_2_MHref_owned",
                "claim": "stable same-frame M_H_ref exists",
                "gate_pass": False,
                "reason": "positive Hamiltonian source denominator is missing",
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3088_3_zero_theorem",
                "claim": "bulk/edge/source residuals vanish by theorem",
                "gate_pass": False,
                "reason": "vertical, source-free, exactness and projector clauses are unsigned",
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3088_4_FB5540_pack_ready",
                "claim": "FB5540 source row is claim-ready",
                "gate_pass": False,
                "reason": "M_H_ref and numerator components remain missing",
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3088_5_Newton_local_GR",
                "claim": "Newton/local-GR gates can reopen",
                "gate_pass": False,
                "reason": "source charge, zero theorem and source pack remain blocked",
                "claim_allowed_for_physics": False,
            },
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "decision_id": "DEC3088_0_contract_result",
                "decision": "PARENT_ACTION_CONTRACT_WRITTEN_NOT_CLOSED",
                "reason": "the exact clauses for L_X,Theta_X,Q_X,B_ref,B_class,tau and M_H_ref are now explicit but not signed by current MTS",
                "next_action": "do not promote FB5540,R10,R11,Newton or local GR from symbolic sector machinery",
            },
            {
                "decision_id": "DEC3088_1_best_derivation_route",
                "decision": "TRY_BOUNDARY_EXACTNESS_PROJECTOR_ORTHOGONALITY_NEXT",
                "reason": "edge/source leakage is the first structural place a theorem might kill residuals without data fitting",
                "next_action": "prove Q_edge exact/proper-gauge and Pi_M^H[Q_edge]=0, or retain edge source coefficients",
            },
            {
                "decision_id": "DEC3088_2_source_fallback",
                "decision": "FULL_NO_CANCELLATION_SOURCE_PACK_REQUIRED_IF_THEOREM_FAILS",
                "reason": "FB5540,bulk X,edge X and R11 components cannot cancel as unknowns or borrow orbital GM as denominator",
                "next_action": "source M_H_ref and all numerator/edge/bulk factors together or keep row blocked",
            },
            {
                "decision_id": "DEC3088_3_no_claim",
                "decision": "NEWTON_LOCAL_GR_NOT_CLAIMED",
                "reason": "owner contract is explicit but no zero theorem or source pack is complete",
                "next_action": "keep all empirical/local gates false",
            },
            {
                "decision_id": "DEC3088_4_best_next",
                "decision": "BOUNDARY_EXACTNESS_PROJECTOR_OR_FB5540_SOURCE_PACK_IS_NEXT",
                "reason": "this is the first route that could either prove residual silence or produce score-ready nonclaim coefficients",
                "next_action": "3089-Y5-R2FR-boundary-exactness-projector-orthogonality-or-FB5540-source-pack-under-AX1090.md",
            },
        ]
    )


def next_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "next_id": "NEXT3088_0_3089",
                "next_checkpoint": "3089-Y5-R2FR-boundary-exactness-projector-orthogonality-or-FB5540-source-pack-under-AX1090.md",
                "script": "scripts/Y5_R2FR_boundary_exactness_projector_orthogonality_or_FB5540_source_pack_under_AX1090_3089.py",
                "mission": "prove boundary exactness/projector orthogonality/no-double-count for the X/Hamiltonian branch, or build a complete FB5540/bulk/edge source pack",
                "starting_equation": "Q_edge=deta and/or Pi_M^H[Q_edge]=0; otherwise alpha_total <= (|FB5540|+|bulk_X|+|edge_X|+|R11|)/M_H_ref",
                "claim_policy": "no Newton/local-GR, R10/R11, PPN, clock or orbital claim unless edge/bulk/source residuals are theorem-zero or source-backed with a no-cancellation guard",
            }
        ]
    )


def branch_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "copy_id": copy_id,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
            }
            for copy_id, (source, destination) in {
                "BR3088_0_owner_clauses": (OUTPUTS["owner_clauses"], BRANCH_OUTPUTS["owner_clauses_copy"]),
                "BR3088_1_source_schema": (OUTPUTS["source_schema"], BRANCH_OUTPUTS["source_schema_copy"]),
                "BR3088_2_guard": (OUTPUTS["guard"], BRANCH_OUTPUTS["guard_copy"]),
                "BR3088_3_bridge": (OUTPUTS["bridge"], BRANCH_OUTPUTS["bridge_copy"]),
                "BR3088_4_next": (OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
            }.items()
        ]
    )


def markdown_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for output_row in output_rows:
        values = [str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    parent_contract: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    guard: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    body = f"""# 3088 - Sector Lagrangian Boundary Owner or FB5540 Source Row

Status: `Y5_R2FR_3088_parent_action_contract_written_not_closed`

## Verdict

This checkpoint writes the exact contract a future parent action must satisfy before the local Newton/GR branch can be claimed: `L_X`, `Theta_X`, `Q_X`, `B_ref`, boundary class/no-hair, tau lock, and a positive same-frame `M_H_ref` must all be owned by one parent variational principle.

Current MTS does not yet sign that contract. The good news is that the gap is no longer vague: either a boundary/projector zero theorem must kill the residual branch, or a complete `FB5540` source pack must be filled with `M_H_ref` and every numerator component under a no-cancellation guard.

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "parse_ok", "needles_present", "missing_needles", "role"])}

## Parent Action Contract

{markdown_table(parent_contract, ["contract_id", "required_clause", "mathematical_form", "current_status", "blocks", "next_action"])}

## Owner Clauses

{markdown_table(owners, ["owner_id", "required_owner", "mathematical_form", "current_status", "failure_if_missing", "feeds"])}

## Theorem Route Tests

{markdown_table(routes, ["route_id", "route", "mathematical_test", "current_status", "if_success", "blocker", "fallback"])}

## FB5540 Source Row Schema

{markdown_table(schema, ["row_id", "quantity", "definition", "required_columns", "current_status"])}

## FB5540 Source Row Runner

{markdown_table(runner, ["runner_id", "row_id", "quantity", "computed_status", "claim_allowed", "failure_reasons"])}

## No-Cancellation Guard

{markdown_table(guard, ["guard_id", "guard", "required_test", "current_status", "claim_impact"])}

## GR Bridge Status

{markdown_table(bridge, ["status_id", "bridge_piece", "current_status", "remaining_gap", "bridge_claim"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed_for_physics"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_target, ["next_id", "next_checkpoint", "script", "mission", "starting_equation", "claim_policy"])}

## Validation

{markdown_table(validation, ["validation_id", "passed", "requirement", "evidence"])}
"""
    DOC.write_text(body, encoding="utf-8")


def validate(generated_paths: list[Path], branch_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows(OUTPUTS["sources"])
    parent_contract = rows(OUTPUTS["parent_contract"])
    owners = rows(OUTPUTS["owner_clauses"])
    routes = rows(OUTPUTS["route_tests"])
    schema = rows(OUTPUTS["source_schema"])
    runner = rows(OUTPUTS["source_runner"])
    guard = rows(OUTPUTS["guard"])
    bridge = rows(OUTPUTS["bridge"])
    gates = rows(OUTPUTS["gates"])
    decisions = rows(OUTPUTS["decisions"])
    next_target = rows(OUTPUTS["next"])

    checks: list[tuple[str, bool, str, str]] = [
        (
            "VAL3088_00_sources_exist",
            all(boolish(row["exists"]) for row in source_rows),
            "all cited source paths exist",
            "P8_Y5_R2FR_3088_SOURCE_REGISTER.csv",
        ),
        (
            "VAL3088_01_needles_present",
            all(boolish(row["needles_present"]) for row in source_rows),
            "all cited source needles are present",
            "P8_Y5_R2FR_3088_SOURCE_REGISTER.csv",
        ),
        (
            "VAL3088_02_sources_parse",
            all(boolish(row["parse_ok"]) for row in source_rows),
            "all cited CSV sources parse and markdown sources exist",
            "P8_Y5_R2FR_3088_SOURCE_REGISTER.csv",
        ),
        (
            "VAL3088_03_csv_parse",
            all(csv_ok(path) for path in generated_paths + branch_paths),
            "all generated and branch-copy CSVs parse cleanly",
            "csv.DictReader parse check",
        ),
        (
            "VAL3088_04_contract_complete",
            len(parent_contract) >= 8 and any(row["contract_id"] == "PAC3088_7_verdict" for row in parent_contract),
            "parent contract includes full verdict row",
            "P8_Y5_R2FR_3088_PARENT_ACTION_CONTRACT.csv",
        ),
        (
            "VAL3088_05_contract_not_claimed",
            any(row["current_status"] == "FAIL_CURRENT_CLAIM" for row in parent_contract),
            "parent contract is written but current-MTS closure remains false",
            "P8_Y5_R2FR_3088_PARENT_ACTION_CONTRACT.csv",
        ),
        (
            "VAL3088_06_owner_map_complete",
            len(owners) >= 9 and any(row["owner_id"] == "LOC3088_7_MHref_owner" for row in owners),
            "owner map covers L_X, Theta/Q, boundary, tau and M_H_ref",
            "P8_Y5_R2FR_3088_OWNER_CLAUSES.csv",
        ),
        (
            "VAL3088_07_owner_map_blocks_claim",
            all(str(row.get("valid_for_claim", "")).lower() == "false" for row in owners),
            "all owner rows remain nonclaim",
            "P8_Y5_R2FR_3088_OWNER_CLAUSES.csv",
        ),
        (
            "VAL3088_08_route_split_written",
            {"RT3088_1_vertical_first_class_zero", "RT3088_2_positive_sourcefree_zero", "RT3088_3_boundary_exact_projector_zero", "RT3088_5_FB5540_source_pack"}.issubset({row["route_id"] for row in routes}),
            "route split covers vertical zero, source-free zero, boundary/projector zero and source fallback",
            "P8_Y5_R2FR_3088_THEOREM_ROUTE_TESTS.csv",
        ),
        (
            "VAL3088_09_route_split_nonclaim",
            all(str(row.get("valid_for_claim", "")).lower() == "false" for row in routes),
            "all route-test rows remain nonclaim",
            "P8_Y5_R2FR_3088_THEOREM_ROUTE_TESTS.csv",
        ),
        (
            "VAL3088_10_source_schema_complete",
            len(schema) == 8 and any(row["row_id"] == "FSR3088_7_total_guard" for row in schema),
            "source schema covers M_H_ref, FB5540 components, bulk X, edge X and total guard",
            "P8_Y5_R2FR_3088_FB5540_SOURCE_ROW_SCHEMA.csv",
        ),
        (
            "VAL3088_11_source_schema_nonclaim",
            all(str(row.get("valid_for_claim", "")).lower() == "false" for row in schema + runner),
            "source schema and runner rows remain nonclaim",
            "P8_Y5_R2FR_3088_FB5540_SOURCE_ROW_SCHEMA.csv;RUNNER.csv",
        ),
        (
            "VAL3088_12_runner_blocked",
            all(row["computed_status"] == "BLOCKED_MISSING_INPUTS" for row in runner),
            "all source runner rows are explicitly blocked by missing theorem/source inputs",
            "P8_Y5_R2FR_3088_FB5540_SOURCE_ROW_RUNNER.csv",
        ),
        (
            "VAL3088_13_no_cancellation_guard",
            len(guard) >= 4 and all(row["current_status"] == "ACTIVE_BAN" for row in guard),
            "no-cancellation, denominator, zero-route and source-pack guards are active",
            "P8_Y5_R2FR_3088_NO_CANCELLATION_GUARD.csv",
        ),
        (
            "VAL3088_14_gr_bridge_blocked",
            all(str(row["bridge_claim"]).lower() == "false" for row in bridge),
            "GR bridge rows remain blocked/nonclaim",
            "P8_Y5_R2FR_3088_GR_BRIDGE_STATUS.csv",
        ),
        (
            "VAL3088_15_claim_gates_blocked",
            all(str(row["claim_allowed_for_physics"]).lower() == "false" for row in gates),
            "no physics claim gate is opened",
            "P8_Y5_R2FR_3088_CLAIM_GATE.csv",
        ),
        (
            "VAL3088_16_newton_gate_false",
            any(row["gate_id"] == "CG3088_5_Newton_local_GR" and str(row["gate_pass"]).lower() == "false" for row in gates),
            "Newton/local-GR gate remains false",
            "P8_Y5_R2FR_3088_CLAIM_GATE.csv",
        ),
        (
            "VAL3088_17_decision_no_claim",
            any(row["decision"] == "NEWTON_LOCAL_GR_NOT_CLAIMED" for row in decisions),
            "decision ledger explicitly refuses Newton/local-GR claim",
            "P8_Y5_R2FR_3088_DECISION_LEDGER.csv",
        ),
        (
            "VAL3088_18_next_target_selected",
            len(next_target) == 1 and next_target[0]["next_id"] == "NEXT3088_0_3089",
            "next target is selected",
            "P8_Y5_R2FR_3088_NEXT_TARGET.csv",
        ),
        (
            "VAL3088_19_branch_copies_exist",
            all(path.exists() for path in branch_paths),
            "branch copy CSVs exist",
            "P8_Y5_R2FR_3088_BRANCH_COPIES.csv",
        ),
        (
            "VAL3088_20_formalization_untouched",
            not any(FORMALIZATION.rglob("*3088*")) if FORMALIZATION.exists() else True,
            "no 3088 files exist under formalization-workbench",
            str(FORMALIZATION),
        ),
        (
            "VAL3088_21_pycache_removed",
            not PYCACHE.exists(),
            "scripts __pycache__ removed",
            str(PYCACHE),
        ),
        (
            "VAL3088_22_doc_written",
            DOC.exists() and "PARENT_ACTION_CONTRACT_WRITTEN_NOT_CLOSED" in text(DOC),
            "checkpoint markdown is written with nonclaim verdict",
            str(DOC),
        ),
    ]
    return with_meta(
        [
            {
                "validation_id": validation_id,
                "passed": passed,
                "requirement": requirement,
                "evidence": evidence,
            }
            for validation_id, passed, requirement, evidence in checks
        ]
    )


def main() -> None:
    remove_pycache()
    for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
        path.parent.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    parent_contract = parent_contract_rows()
    owners = owner_clause_rows()
    routes = route_test_rows()
    schema = source_schema_rows()
    runner = source_runner_rows(schema)
    guard = guard_rows()
    bridge = bridge_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["parent_contract"], parent_contract)
    write_csv(OUTPUTS["owner_clauses"], owners)
    write_csv(OUTPUTS["route_tests"], routes)
    write_csv(OUTPUTS["source_schema"], schema)
    write_csv(OUTPUTS["source_runner"], runner)
    write_csv(OUTPUTS["guard"], guard)
    write_csv(OUTPUTS["bridge"], bridge)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    copy_map = {
        OUTPUTS["owner_clauses"]: BRANCH_OUTPUTS["owner_clauses_copy"],
        OUTPUTS["source_schema"]: BRANCH_OUTPUTS["source_schema_copy"],
        OUTPUTS["guard"]: BRANCH_OUTPUTS["guard_copy"],
        OUTPUTS["bridge"]: BRANCH_OUTPUTS["bridge_copy"],
        OUTPUTS["next"]: BRANCH_OUTPUTS["next_copy"],
    }
    for source, destination in copy_map.items():
        shutil.copyfile(source, destination)

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    generated_paths = [path for key, path in OUTPUTS.items() if key not in {"validation"}]
    branch_paths = list(BRANCH_OUTPUTS.values())
    validation = validate(generated_paths, branch_paths)
    write_doc(sources, parent_contract, owners, routes, schema, runner, guard, bridge, gates, decisions, next_target, validation)
    validation = validate(generated_paths, branch_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, parent_contract, owners, routes, schema, runner, guard, bridge, gates, decisions, next_target, validation)

    remove_pycache()
    validation = validate(generated_paths, branch_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, parent_contract, owners, routes, schema, runner, guard, bridge, gates, decisions, next_target, validation)

    failed = [row for row in validation if not boolish(row["passed"])]
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    print(f"Validation passed {len(validation) - len(failed)}/{len(validation)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['validation_id']}: {row['requirement']} ({row['evidence']})")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
