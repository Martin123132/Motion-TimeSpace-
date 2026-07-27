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

CHECKPOINT = "3089"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3089-Y5-R2FR-boundary-exactness-projector-orthogonality-or-FB5540-source-pack-under-AX1090.md"

SOURCES = {
    "SRC3089_00_3088_doc": {
        "path": ROOT / "3088-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row-under-AX1090.md",
        "needles": ["boundary/projector zero theorem", "FB5540"],
        "role": "3088 selects boundary/projector zero theorem or FB5540 source pack.",
    },
    "SRC3089_01_3088_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3088_NEXT_TARGET.csv",
        "needles": ["NEXT3088_0_3089", "Q_edge=deta"],
        "role": "3088 handoff names this 3089 boundary/projector target.",
    },
    "SRC3089_02_3088_routes": {
        "path": RESIDUALS / "P8_Y5_R2FR_3088_THEOREM_ROUTE_TESTS.csv",
        "needles": ["RT3088_3_boundary_exact_projector_zero", "PRECISE_BUT_PARENT_UNSIGNED"],
        "role": "3088 route split keeps boundary/projector zero conditional.",
    },
    "SRC3089_03_1843_precedent": {
        "path": ROOT / "1843-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["WEIGHTED_STOKES_IS_THE_CORRECT_LOCAL_BOUND_LAW", "BX_PRIMITIVE_FROM_PARENT_VARIATION"],
        "role": "1843 precedent derives weighted Stokes as the honest fallback.",
    },
    "SRC3089_04_1019_exactness": {
        "path": RESIDUALS / "P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv",
        "needles": ["BE1019_1_BX_exact", "kernel_derivative_terms"],
        "role": "1019 boundary exactness clauses.",
    },
    "SRC3089_05_1019_projector": {
        "path": RESIDUALS / "P8_Y5_R10_1019_PROJECTOR_ORTHOGONALITY_CLAUSES.csv",
        "needles": ["PO1019_0_projector_definition", "Qbar_edge_XH"],
        "role": "1019 projector orthogonality clauses.",
    },
    "SRC3089_06_1019_source_pack": {
        "path": RESIDUALS / "P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv",
        "needles": ["SP1019_0_M_H_ref", "MISSING_FB5540_COMPONENT_VALUES"],
        "role": "1019 source-pack schema for M_H_ref, FB5540, bulk and edge rows.",
    },
    "SRC3089_07_1020_domain": {
        "path": RESIDUALS / "P8_Y5_R10_1020_BOUNDARY_DOMAIN_CERTIFICATE.csv",
        "needles": ["BDC1020_2_relative_cohomology", "kernel_derivative_bound"],
        "role": "1020 boundary domain/cohomology certificate.",
    },
    "SRC3089_08_1020_BX": {
        "path": RESIDUALS / "P8_Y5_R10_1020_BX_PRIMITIVE_AUDIT.csv",
        "needles": ["BXP1020_2_exact_primitive", "b_X_norm"],
        "role": "1020 B_X primitive audit identifies the next hard object.",
    },
    "SRC3089_09_1020_doc": {
        "path": ROOT / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
        "needles": ["weighted-Stokes theorem", "B_X=d_S b_X"],
        "role": "1020 markdown states the weighted-Stokes local condition.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3089_SOURCE_REGISTER.csv",
    "boundary": RESIDUALS / "P8_Y5_R2FR_3089_BOUNDARY_EXACTNESS_CLAUSES.csv",
    "projector": RESIDUALS / "P8_Y5_R2FR_3089_PROJECTOR_ORTHOGONALITY_CLAUSES.csv",
    "domain": RESIDUALS / "P8_Y5_R2FR_3089_BOUNDARY_DOMAIN_CERTIFICATE.csv",
    "stokes": RESIDUALS / "P8_Y5_R2FR_3089_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv",
    "source_pack": RESIDUALS / "P8_Y5_R2FR_3089_SOURCE_PACK_SCHEMA.csv",
    "route_verdicts": RESIDUALS / "P8_Y5_R2FR_3089_ROUTE_VERDICTS.csv",
    "bridge": RESIDUALS / "P8_Y5_R2FR_3089_GR_BRIDGE_STATUS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3089_CLAIM_GATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3089_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3089_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3089_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3089_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "boundary_copy": LOCAL_BOUNDS / "boundary_exactness_clauses_3089_NONCLAIM.csv",
    "projector_copy": LOCAL_BOUNDS / "projector_orthogonality_clauses_3089_NONCLAIM.csv",
    "stokes_copy": LOCAL_BOUNDS / "weighted_stokes_bound_3089_NONCLAIM.csv",
    "source_pack_copy": LOCAL_BOUNDS / "FB5540_bulk_edge_source_pack_3089_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3089_BX_primitive_or_edge_bound_NEXT_NONCLAIM.csv",
}


def meta() -> dict[str, Any]:
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
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


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


def with_meta(output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base = meta()
    return [{**base, **output_row} for output_row in output_rows]


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


def source_rows() -> list[dict[str, Any]]:
    output_rows = []
    for source_id, source in SOURCES.items():
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


def boundary_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "clause_id": "BE3089_0_domain",
                "claim": "edge integration domain has no untracked corner or domain dependence",
                "mathematical_form": "partial S_edge=empty, or every corner C carries explicit Q_C in source pack",
                "current_status": "NOT_SIGNED",
                "what_would_close": "parent boundary class fixes S_edge and corner terms before readout",
                "failure_mode": "Stokes zero hides corner/domain charge",
            },
            {
                "clause_id": "BE3089_1_exact_BX",
                "claim": "boundary momentum is exact on the certified boundary class",
                "mathematical_form": "B_X=d_S b_X with no residual r_X and no harmonic h_X",
                "current_status": "NOT_DERIVED",
                "what_would_close": "derive b_X from parent L_X/Theta_X/Q_X plus fixed counterterm",
                "failure_mode": "Q_edge remains live or must be bounded",
            },
            {
                "clause_id": "BE3089_2_weight_kernel_closed",
                "claim": "weighted Stokes has no surface-derivative leakage",
                "mathematical_form": "d_S(F_lambda epsilon_X)=0 on S_edge or ||d_S(F_lambda epsilon_X)||_* is source-bounded",
                "current_status": "NOT_SIGNED",
                "what_would_close": "kernel/gauge weight is fixed by parent boundary class and cannot vary with source readout",
                "failure_mode": "exact B_X still leaves derivative term",
            },
            {
                "clause_id": "BE3089_3_no_harmonic_residual",
                "claim": "harmonic and non-owned residual edge pieces vanish or are measured",
                "mathematical_form": "B_X=d_S b_X+h_X+r_X with h_X=0 and r_X=0, or both source-bounded",
                "current_status": "NOT_SIGNED",
                "what_would_close": "parent cohomology certificate kills H_edge or supplies h_X/r_X rows",
                "failure_mode": "harmonic/residual edge mode survives exactness",
            },
            {
                "clause_id": "BE3089_4_reference_silent",
                "claim": "boundary/reference class is fixed under source variation",
                "mathematical_form": "partial_{M_H_ref,tau,reference,surface} B_class = 0",
                "current_status": "NOT_SIGNED",
                "what_would_close": "B_ref and B_class selected before readout by parent principle",
                "failure_mode": "edge charge is moved into source normalization",
            },
            {
                "clause_id": "BE3089_5_verdict",
                "claim": "boundary exactness kills edge branch",
                "mathematical_form": "BE3089_0 through BE3089_4 imply Q_edge^H(lambda)=0 and K_boundary=0",
                "current_status": "FAIL_CURRENT_CLAIM",
                "what_would_close": "all exactness clauses parent-signed in one boundary class",
                "failure_mode": "retain weighted-Stokes/source-pack rows for Qbar_edge_XH and K_edge",
            },
        ]
    )


def projector_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "clause_id": "PO3089_0_projector_definition",
                "claim": "Pi_M^H is the fixed Hamiltonian source-mass projector",
                "mathematical_form": "Pi_M^H[J]=partial J/partial M_H_ref at fixed tau, reference, surface, C_top and chi_B",
                "current_status": "NOT_SIGNED",
                "what_would_close": "M_H_ref and Pi_M^H defined from parent Hamiltonian charge before readout",
                "failure_mode": "projector can select wrong object",
            },
            {
                "clause_id": "PO3089_1_edge_mass_independence",
                "claim": "edge charge has no same-frame source-mass dependence",
                "mathematical_form": "partial Q_edge^H(lambda)/partial M_H_ref |_{tau,reference,surface}=0",
                "current_status": "NOT_DERIVED",
                "what_would_close": "Q_edge depends only on fixed boundary cohomology/gauge data",
                "failure_mode": "Qbar_edge_XH(lambda) remains live",
            },
            {
                "clause_id": "PO3089_2_symplectic_block",
                "claim": "source and edge sectors are symplectically orthogonal",
                "mathematical_form": "Omega(delta_M Phi,delta_edge Phi)=0 and Pi_M^H[delta_edge Q]=0",
                "current_status": "NOT_DERIVED",
                "what_would_close": "block-diagonal reduced symplectic form or exact mixed term",
                "failure_mode": "edge/source mixing feeds FB5540 or R10/R11",
            },
            {
                "clause_id": "PO3089_3_reference_silence",
                "claim": "reference subtraction does not reroute edge charge into mass readout",
                "mathematical_form": "Pi_M^H[Delta_ref+Delta_symp+B_class]=0",
                "current_status": "NOT_SIGNED",
                "what_would_close": "B_ref derivative-silent theorem plus boundary class certificate",
                "failure_mode": "projector orthogonality broken by reference movement",
            },
            {
                "clause_id": "PO3089_4_conditional_zero",
                "claim": "projector clauses kill edge Hamiltonian source charge",
                "mathematical_form": "PO3089_0 through PO3089_3 imply Qbar_edge_XH(lambda)=0",
                "current_status": "CONDITIONAL_THEOREM_ONLY",
                "what_would_close": "parent-signed projector definition, mass-independence, symplectic block and reference lemmas",
                "failure_mode": "cannot zero edge projection row",
            },
            {
                "clause_id": "PO3089_5_verdict",
                "claim": "projector orthogonality kills edge source projection",
                "mathematical_form": "Pi_M^H[Q_edge]=0 with no reference, tau or surface leakage",
                "current_status": "FAIL_CURRENT_CLAIM",
                "what_would_close": "PO3089_0 through PO3089_4 signed by same parent action/boundary class",
                "failure_mode": "retain Qbar_edge_XH source-pack row",
            },
        ]
    )


def domain_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "certificate_id": "BDC3089_0_surface_manifold",
                "object": "edge surface S_edge",
                "required_certificate": "compact oriented smooth codim-2 surface with no active corner boundary",
                "mathematical_test": "partial S_edge=empty or every corner C has explicit corner charge Q_C",
                "current_status": "NOT_SIGNED",
                "failure_if_missing": "Stokes zero can hide corner charge",
                "feeds": "Q_edge_zero;corner_source_row",
            },
            {
                "certificate_id": "BDC3089_1_boundary_class",
                "object": "allowed boundary class B_class",
                "required_certificate": "same B_class used by L_X,Q_X,B_ref,Pi_M^H and R10/R11 readout",
                "mathematical_test": "delta B_class=0 along source variation and no retuning between source/test systems",
                "current_status": "NOT_SIGNED",
                "failure_if_missing": "reference or boundary class can absorb the signal",
                "feeds": "FB5540;Qbar_edge_XH",
            },
            {
                "certificate_id": "BDC3089_2_relative_cohomology",
                "object": "relative edge cohomology H_edge",
                "required_certificate": "harmonic/non-exact edge class absent or separately measured as h_X",
                "mathematical_test": "B_X=d_S b_X+h_X with h_X=0, or |int_S F_lambda epsilon h_X| source-bounded",
                "current_status": "NOT_SIGNED",
                "failure_if_missing": "exactness misses a harmonic edge mode",
                "feeds": "harmonic_edge_bound;Q_edge_zero",
            },
            {
                "certificate_id": "BDC3089_3_allowed_epsilon",
                "object": "epsilon_X domain",
                "required_certificate": "epsilon_X is a proper X-representative gauge while tau/mass/rotation remain admissible",
                "mathematical_test": "epsilon_X|S_edge=0 or d_S(F_lambda epsilon_X)=0 without constraining tau_source or ADM charges",
                "current_status": "CLOSURE_ONLY",
                "failure_if_missing": "proper-gauge zero may erase real physical charges",
                "feeds": "Q_edge_zero;projector_definition",
            },
            {
                "certificate_id": "BDC3089_4_kernel_weight",
                "object": "F_lambda epsilon_X",
                "required_certificate": "edge kernel/gauge weight is closed on S_edge or derivative term is source-bounded",
                "mathematical_test": "d_S(F_lambda epsilon_X)=0, or ||d_S(F_lambda epsilon_X)||_* and ||b_X||_* are supplied",
                "current_status": "NOT_SIGNED",
                "failure_if_missing": "weighted Stokes identity leaves a derivative residual",
                "feeds": "kernel_derivative_bound",
            },
            {
                "certificate_id": "BDC3089_5_verdict",
                "object": "boundary domain certificate",
                "required_certificate": "BDC3089_0 through BDC3089_4 signed in one parent boundary class",
                "mathematical_test": "closed/corner-free plus cohomology plus epsilon/kernel conditions imply no untracked edge domain term",
                "current_status": "FAIL_CURRENT_CLAIM",
                "failure_if_missing": "Q_edge cannot be set to zero by Stokes alone",
                "feeds": "3090_BX_primitive_or_edge_bound",
            },
        ]
    )


def stokes_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "theorem_id": "ETB3089_0_decomposition",
                "statement": "boundary momentum decomposes into exact, harmonic and residual pieces",
                "formula": "B_X=d_S b_X+h_X+r_X",
                "current_result": "FORMAL_DECOMPOSITION",
                "missing_for_claim": "parent L_X/Theta_X/Q_X must prove r_X=0 and identify h_X",
                "bound_if_missing": "||Q_edge|| keeps |int_S F epsilon h_X| + |int_S F epsilon r_X|",
            },
            {
                "theorem_id": "ETB3089_1_weighted_Stokes_identity",
                "statement": "exactness kills edge charge only when kernel/gauge weight has no surface derivative term",
                "formula": "int_S F epsilon d_S b_X = int_partialS F epsilon b_X - int_S d_S(F epsilon) wedge b_X",
                "current_result": "MATH_IDENTITY_WRITTEN",
                "missing_for_claim": "partialS=empty or corner row, plus d_S(F epsilon)=0 or derivative bound",
                "bound_if_missing": "|int_S F epsilon d_S b_X| <= ||d_S(F epsilon)||_* ||b_X||_* + |corner_term|",
            },
            {
                "theorem_id": "ETB3089_2_zero_conditions",
                "statement": "genuine edge-zero theorem needs exactness, no harmonic/residual/corner terms and closed weight",
                "formula": "partialS=empty, h_X=0, r_X=0, d_S(F epsilon)=0 => Q_edge^H(lambda)=0",
                "current_result": "CONDITIONAL_THEOREM",
                "missing_for_claim": "all hypotheses unsigned in current MTS",
                "bound_if_missing": "use ETB3089_3 residual bound instead of zero",
            },
            {
                "theorem_id": "ETB3089_3_residual_bound",
                "statement": "if exact zero fails, edge charge has a finite source-pack bound",
                "formula": "||Q_edge(lambda)|| <= C_corner + ||d_S(F_lambda epsilon_X)||_* ||b_X||_* + |int_S F_lambda epsilon_X h_X| + |int_S F_lambda epsilon_X r_X|",
                "current_result": "BOUND_LAW_STAGED",
                "missing_for_claim": "numeric/source-backed norms for each term and units",
                "bound_if_missing": "first nonclaim source row stores terms with valid_for_claim=false",
            },
            {
                "theorem_id": "ETB3089_4_projector_bound",
                "statement": "Hamiltonian/source projection is bounded after M_H_ref and Pi_M norm are owned",
                "formula": "||Qbar_edge_XH(lambda)|| <= ||Pi_M^H|| ||Q_edge(lambda)|| / M_H_ref_min",
                "current_result": "CONDITIONAL_BOUND",
                "missing_for_claim": "Pi_M^H definition, M_H_ref_min and source-backed Q_edge bound",
                "bound_if_missing": "Qbar_edge_XH remains MISSING_SOURCE_BACKED_QBAR_EDGE_XH",
            },
            {
                "theorem_id": "ETB3089_5_verdict",
                "statement": "exact local condition and fallback bound are derived, but not the zero theorem",
                "formula": "Q_edge=0 conditional; Q_edge_bound schema-ready; no claim promoted",
                "current_result": "FAIL_CURRENT_CLAIM_BUT_DERIVATION_PROGRESS",
                "missing_for_claim": "B_X primitive, h_X/r_X zero or bounds, kernel derivative bound, corner audit, M_H_ref/Pi_M",
                "bound_if_missing": "move to 3090 B_X primitive or first source-bound term",
            },
        ]
    )


def source_pack_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "pack_id": "SP3089_0_M_H_ref",
                "quantity": "M_H_ref",
                "definition": "same-frame Hamiltonian source denominator",
                "required_columns": "system_id;tau_id;surface;Q_tau_integral;G_ref;H_ref;M_H_ref;units;reference_rule;source_path;valid_for_claim",
                "current_status": "MISSING_STABLE_MH_REF",
            },
            {
                "pack_id": "SP3089_1_FB5540_components",
                "quantity": "delta_H_tau_nonintegrable_over_MH;Delta_ref_over_MH;symplectic_boundary_flux_over_MH",
                "definition": "componentwise FB5540 numerator rows normalized by M_H_ref",
                "required_columns": "system_id;component_id;value_abs;M_H_ref;units;source_path;assumptions;valid_for_claim",
                "current_status": "MISSING_FB5540_COMPONENT_VALUES",
            },
            {
                "pack_id": "SP3089_2_edge_bound_terms",
                "quantity": "C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs",
                "definition": "weighted-Stokes bound terms for Q_edge(lambda)",
                "required_columns": "system_id;lambda;C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs;units;source_path;valid_for_claim",
                "current_status": "MISSING_EDGEBOUND_TERMS",
            },
            {
                "pack_id": "SP3089_3_projected_edge_bound",
                "quantity": "Qbar_edge_XH_bound(lambda)",
                "definition": "projected edge bound after Pi_M^H norm and M_H_ref_min",
                "required_columns": "system_id;lambda;PiM_norm;Q_edge_bound;M_H_ref_min;Qbar_edge_XH_bound;units;source_path;valid_for_claim",
                "current_status": "MISSING_PIM_NORM_OR_MHREF_MIN",
            },
            {
                "pack_id": "SP3089_4_bulk_X_coefficients",
                "quantity": "Z_X;M_X2;J_X;lambda_X;K_X;Qbar_XH;qbar_XT",
                "definition": "bulk X residual coefficients if no-pole/source-free theorem fails",
                "required_columns": "system_id;field_id;Z_X;M_X2;J_X;lambda_X;K_X;Qbar_XH;qbar_XT;units;source_path;valid_for_claim",
                "current_status": "MISSING_PARENT_INPUT_OR_ARENA_PROJECTION",
            },
            {
                "pack_id": "SP3089_5_edge_coefficients",
                "quantity": "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge(lambda)",
                "definition": "edge residual amplitude if boundary/projector theorem fails",
                "required_columns": "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge;units;source_path;valid_for_claim",
                "current_status": "MISSING_EDGE_PROJECTION",
            },
            {
                "pack_id": "SP3089_6_total_guard",
                "quantity": "alpha_total_guard(lambda)",
                "definition": "absolute no-cancellation envelope across FB5540, bulk X, edge X and R11",
                "required_columns": "system_id;lambda;abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_alpha_R11;component_sum_abs;bound;source_path;valid_for_claim",
                "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            },
        ]
    )


def route_verdict_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "route_id": "RVT3089_0_boundary_exactness",
                "route": "derive Q_edge=0 from exact boundary form",
                "status": "CONDITIONAL_NOT_PROMOTED",
                "requires": "BE3089 clauses plus BDC3089 certificates and ETB3089 zero conditions",
                "result": "FAIL_CURRENT_CLAIM",
                "fallback": "retain edge source-pack rows",
            },
            {
                "route_id": "RVT3089_1_projector_orthogonality",
                "route": "derive Qbar_edge_XH=0 from mass-projector orthogonality",
                "status": "CONDITIONAL_NOT_PROMOTED",
                "requires": "PO3089 clauses plus M_H_ref/Pi_M^H owner",
                "result": "FAIL_CURRENT_CLAIM",
                "fallback": "source or bound Pi_M^H[Q_edge]",
            },
            {
                "route_id": "RVT3089_2_weighted_stokes_bound",
                "route": "replace closure axiom with weighted-Stokes residual bound",
                "status": "BOUND_LAW_DERIVED_SCHEMA_READY",
                "requires": "C_corner,norm_dS_Feps,norm_bX,harmonic_edge_abs,residual_edge_abs,M_H_ref_min,PiM_norm",
                "result": "NONCLAIM_SOURCE_PACK_REQUIRED",
                "fallback": "3090 B_X primitive or first bound term",
            },
            {
                "route_id": "RVT3089_3_no_double_count",
                "route": "orthogonal source split prevents duplicate scoring",
                "status": "GUARD_WRITTEN_NOT_DERIVED",
                "requires": "bulk/edge/FB5540/R11 projectors and source currents",
                "result": "BLOCKS_CURRENT_CLAIM",
                "fallback": "absolute no-cancellation envelope",
            },
            {
                "route_id": "RVT3089_4_verdict",
                "route": "3089 branch closure",
                "status": "FAIL_CURRENT_CLAIM_BUT_NARROWS_GAP",
                "requires": "theorem-zero route or complete source pack",
                "result": "no R10/R11/Newton/local-GR pass",
                "fallback": "3090 explicit B_X primitive from parent variation or edge-bound term fill",
            },
        ]
    )


def bridge_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "status_id": "GB3089_0_boundary_zero",
                "bridge_piece": "boundary exactness zero",
                "current_status": "CONDITIONAL_NOT_PROMOTED",
                "evidence": "BE3089;BDC3089;ETB3089",
                "remaining_gap": "domain, B_X primitive, harmonic/residual, kernel-weight and reference clauses unsigned",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3089_1_projector_zero",
                "bridge_piece": "edge-source projector orthogonality",
                "current_status": "CONDITIONAL_NOT_PROMOTED",
                "evidence": "PO3089",
                "remaining_gap": "Pi_M^H, M_H_ref, source/edge symplectic block and reference silence unsigned",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3089_2_source_pack",
                "bridge_piece": "FB5540/bulk/edge/R11 source pack",
                "current_status": "SCHEMA_READY_NO_VALUES",
                "evidence": "SP3089 rows",
                "remaining_gap": "all source-backed numeric/theorem-zero terms missing",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3089_3_Newton_GR",
                "bridge_piece": "Newton/local-GR bridge",
                "current_status": "BLOCKED",
                "evidence": "RVT3089_4",
                "remaining_gap": "edge/source leakage and M_H_ref normalization still open",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3089_4_next",
                "bridge_piece": "next derivation owner",
                "current_status": "BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_IS_NEXT",
                "evidence": "ETB3089_5;1020 B_X primitive audit",
                "remaining_gap": "derive explicit b_X primitive or fill first weighted-Stokes bound term",
                "bridge_claim": False,
            },
        ]
    )


def gate_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "gate_id": "CG3089_0_boundary_exactness_closed",
                "claim": "boundary exactness theorem closes Q_edge",
                "gate_pass": False,
                "reason": "domain, B_X primitive, harmonic/residual, kernel-weight and reference clauses are unsigned",
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3089_1_projector_orthogonality_closed",
                "claim": "projector orthogonality theorem closes Qbar_edge_XH",
                "gate_pass": False,
                "reason": "Pi_M^H definition, edge mass-independence, symplectic block and reference silence are unsigned",
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3089_2_weighted_stokes_zero",
                "claim": "weighted Stokes gives Q_edge=0",
                "gate_pass": False,
                "reason": "d_S(F_lambda epsilon_X)=0, h_X=r_X=0 and no-corner conditions are not proved",
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3089_3_source_pack_complete",
                "claim": "FB5540/bulk/edge/R11 source pack is complete",
                "gate_pass": False,
                "reason": "source pack rows remain missing or not computed",
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3089_4_first_bound_schema_staged",
                "claim": "first edge bound schema is staged as nonclaim",
                "gate_pass": True,
                "reason": "weighted-Stokes bound terms are explicit but missing source values",
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3089_5_Newton_local_GR",
                "claim": "Newton/local-GR gates can reopen",
                "gate_pass": False,
                "reason": "edge/source leakage, source pack and M_H_ref remain open",
                "claim_allowed_for_physics": False,
            },
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "decision_id": "DEC3089_0_theorem_attempt",
                "decision": "BOUNDARY_PROJECTOR_ROUTE_PRECISE_BUT_NOT_CLOSED",
                "reason": "Stokes/projector arguments can kill edge leakage only after boundary domain, B_X primitive, cohomology, kernel and reference clauses are parent-signed",
                "next_action": "derive explicit B_X primitive from parent variation or fill bound terms",
            },
            {
                "decision_id": "DEC3089_1_weighted_stokes",
                "decision": "WEIGHTED_STOKES_IS_THE_CORRECT_LOCAL_BOUND_LAW",
                "reason": "exactness alone is insufficient when F_lambda epsilon_X has a surface derivative, harmonic piece, residual piece, or corner term",
                "next_action": "carry C_corner, norm_dS_Feps, norm_bX, harmonic_edge_abs and residual_edge_abs explicitly",
            },
            {
                "decision_id": "DEC3089_2_projector",
                "decision": "PROJECTOR_ZERO_NEEDS_MHREF_AND_SYMPLECTIC_BLOCK",
                "reason": "Pi_M^H[Q_edge]=0 is not meaningful until M_H_ref and the fixed source-mass projector are owned",
                "next_action": "keep Qbar_edge_XH as nonclaim row unless projector theorem is signed",
            },
            {
                "decision_id": "DEC3089_3_no_claim",
                "decision": "NO_LOCAL_GR_OR_EMPIRICAL_PASS",
                "reason": "zero theorem and source pack are incomplete",
                "next_action": "do not score R10/R11/PPN/clock/orbital branches from 3089",
            },
            {
                "decision_id": "DEC3089_4_best_next",
                "decision": "BX_PRIMITIVE_OR_FIRST_EDGE_BOUND_TERM_IS_NEXT",
                "reason": "B_X=d_S b_X+h_X+r_X is now the concrete object controlling the edge/source leak",
                "next_action": "3090-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-under-AX1090.md",
            },
        ]
    )


def next_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "next_id": "NEXT3089_0_3090",
                "next_checkpoint": "3090-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-under-AX1090.md",
                "script": "scripts/Y5_R2FR_BX_primitive_from_parent_variation_or_edge_bound_term_under_AX1090_3090.py",
                "mission": "derive explicit B_X=d_S b_X+h_X+r_X from parent variation and prove h_X=r_X=0/closed kernel, or fill first weighted-Stokes bound row",
                "starting_equation": "||Q_edge(lambda)|| <= C_corner + ||d_S(F_lambda epsilon_X)||_* ||b_X||_* + |int_S F_lambda epsilon_X h_X| + |int_S F_lambda epsilon_X r_X|",
                "claim_policy": "no edge-zero, projector-zero, R10/R11, Newton/local-GR, PPN, clock or orbital claim until B_X primitive/edge-bound terms are source-backed or theorem-zero",
            }
        ]
    )


def branch_rows() -> list[dict[str, Any]]:
    mapping = {
        "BR3089_0_boundary": (OUTPUTS["boundary"], BRANCH_OUTPUTS["boundary_copy"]),
        "BR3089_1_projector": (OUTPUTS["projector"], BRANCH_OUTPUTS["projector_copy"]),
        "BR3089_2_stokes": (OUTPUTS["stokes"], BRANCH_OUTPUTS["stokes_copy"]),
        "BR3089_3_source_pack": (OUTPUTS["source_pack"], BRANCH_OUTPUTS["source_pack_copy"]),
        "BR3089_4_next": (OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    }
    return with_meta(
        [
            {
                "copy_id": copy_id,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
            }
            for copy_id, (source, destination) in mapping.items()
        ]
    )


def table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for output_row in output_rows:
        lines.append("| " + " | ".join(str(output_row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    projector: list[dict[str, Any]],
    domain: list[dict[str, Any]],
    stokes: list[dict[str, Any]],
    source_pack: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    body = f"""# 3089 - Boundary Exactness Projector Orthogonality or FB5540 Source Pack

Status: `Y5_R2FR_3089_weighted_stokes_bound_law_staged_nonclaim`

## Verdict

The boundary/projector route is mathematically sharper, but it does not yet close current MTS. `Q_edge=0` requires a certified boundary domain, an explicit `B_X=d_S b_X+h_X+r_X` decomposition, no corner/harmonic/residual leakage, a closed kernel weight `d_S(F_lambda epsilon_X)=0`, and a fixed source-mass projector `Pi_M^H` built from the same `M_H_ref`.

The useful result is the fallback law: if exactness or projector orthogonality fails, the edge/source residual is bounded by weighted-Stokes terms instead of erased by a closure axiom.

## Source Register

{table(sources, ["source_id", "source_path", "exists", "parse_ok", "needles_present", "missing_needles", "role"])}

## Boundary Exactness Clauses

{table(boundary, ["clause_id", "claim", "mathematical_form", "current_status", "what_would_close", "failure_mode"])}

## Projector Orthogonality Clauses

{table(projector, ["clause_id", "claim", "mathematical_form", "current_status", "what_would_close", "failure_mode"])}

## Boundary Domain Certificate

{table(domain, ["certificate_id", "object", "required_certificate", "mathematical_test", "current_status", "failure_if_missing", "feeds"])}

## Weighted Stokes Theorem And Bound

{table(stokes, ["theorem_id", "statement", "formula", "current_result", "missing_for_claim", "bound_if_missing"])}

## Source Pack Schema

{table(source_pack, ["pack_id", "quantity", "definition", "required_columns", "current_status"])}

## Route Verdicts

{table(routes, ["route_id", "route", "status", "requires", "result", "fallback"])}

## GR Bridge Status

{table(bridge, ["status_id", "bridge_piece", "current_status", "remaining_gap", "bridge_claim"])}

## Claim Gates

{table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed_for_physics"])}

## Decisions

{table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{table(next_target, ["next_id", "next_checkpoint", "script", "mission", "starting_equation", "claim_policy"])}

## Validation

{table(validation, ["validation_id", "passed", "requirement", "evidence"])}
"""
    DOC.write_text(body, encoding="utf-8")


def validate(generated_paths: list[Path], branch_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows(OUTPUTS["sources"])
    boundary = rows(OUTPUTS["boundary"])
    projector = rows(OUTPUTS["projector"])
    domain = rows(OUTPUTS["domain"])
    stokes = rows(OUTPUTS["stokes"])
    source_pack = rows(OUTPUTS["source_pack"])
    routes = rows(OUTPUTS["route_verdicts"])
    bridge = rows(OUTPUTS["bridge"])
    gates = rows(OUTPUTS["gates"])
    decisions = rows(OUTPUTS["decisions"])
    next_target = rows(OUTPUTS["next"])

    checks = [
        ("VAL3089_00_sources_exist", all(boolish(row["exists"]) for row in sources), "all cited source paths exist", "P8_Y5_R2FR_3089_SOURCE_REGISTER.csv"),
        ("VAL3089_01_needles_present", all(boolish(row["needles_present"]) for row in sources), "all cited source needles are present", "P8_Y5_R2FR_3089_SOURCE_REGISTER.csv"),
        ("VAL3089_02_sources_parse", all(boolish(row["parse_ok"]) for row in sources), "all cited CSV sources parse and markdown sources exist", "P8_Y5_R2FR_3089_SOURCE_REGISTER.csv"),
        ("VAL3089_03_csv_parse", all(csv_ok(path) for path in generated_paths + branch_paths), "all generated and branch-copy CSVs parse cleanly", "csv.DictReader parse check"),
        ("VAL3089_04_boundary_verdict_false", any(row["clause_id"] == "BE3089_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in boundary), "boundary exactness verdict remains false", "P8_Y5_R2FR_3089_BOUNDARY_EXACTNESS_CLAUSES.csv"),
        ("VAL3089_05_projector_verdict_false", any(row["clause_id"] == "PO3089_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in projector), "projector orthogonality verdict remains false", "P8_Y5_R2FR_3089_PROJECTOR_ORTHOGONALITY_CLAUSES.csv"),
        ("VAL3089_06_domain_certificate_complete", len(domain) >= 6 and any(row["certificate_id"] == "BDC3089_5_verdict" for row in domain), "domain certificate covers surface, boundary class, cohomology, epsilon and kernel", "P8_Y5_R2FR_3089_BOUNDARY_DOMAIN_CERTIFICATE.csv"),
        ("VAL3089_07_weighted_stokes_identity", any(row["theorem_id"] == "ETB3089_1_weighted_Stokes_identity" and "d_S(F epsilon)" in row["formula"] for row in stokes), "weighted Stokes identity is recorded", "P8_Y5_R2FR_3089_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv"),
        ("VAL3089_08_residual_bound_staged", any(row["theorem_id"] == "ETB3089_3_residual_bound" and row["current_result"] == "BOUND_LAW_STAGED" for row in stokes), "residual bound is staged rather than erased", "P8_Y5_R2FR_3089_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv"),
        ("VAL3089_09_stokes_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in stokes), "weighted Stokes rows remain nonclaim", "P8_Y5_R2FR_3089_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv"),
        ("VAL3089_10_source_pack_complete", len(source_pack) == 7 and any(row["pack_id"] == "SP3089_6_total_guard" for row in source_pack), "source pack covers M_H_ref, FB5540, edge, bulk and total guard", "P8_Y5_R2FR_3089_SOURCE_PACK_SCHEMA.csv"),
        ("VAL3089_11_source_pack_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in source_pack), "source-pack rows remain nonclaim", "P8_Y5_R2FR_3089_SOURCE_PACK_SCHEMA.csv"),
        ("VAL3089_12_route_verdict", any(row["route_id"] == "RVT3089_4_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_BUT_NARROWS_GAP" for row in routes), "route verdict records failure plus narrowing", "P8_Y5_R2FR_3089_ROUTE_VERDICTS.csv"),
        ("VAL3089_13_bridge_nonclaim", all(str(row["bridge_claim"]).lower() == "false" for row in bridge), "GR bridge rows remain nonclaim", "P8_Y5_R2FR_3089_GR_BRIDGE_STATUS.csv"),
        ("VAL3089_14_claim_gates_blocked", all(str(row["claim_allowed_for_physics"]).lower() == "false" for row in gates), "no physics claim gate is opened", "P8_Y5_R2FR_3089_CLAIM_GATE.csv"),
        ("VAL3089_15_first_schema_only", any(row["gate_id"] == "CG3089_4_first_bound_schema_staged" and str(row["gate_pass"]).lower() == "true" for row in gates), "only schema staging gate passes", "P8_Y5_R2FR_3089_CLAIM_GATE.csv"),
        ("VAL3089_16_newton_gate_false", any(row["gate_id"] == "CG3089_5_Newton_local_GR" and str(row["gate_pass"]).lower() == "false" for row in gates), "Newton/local-GR gate remains false", "P8_Y5_R2FR_3089_CLAIM_GATE.csv"),
        ("VAL3089_17_decision_weighted_stokes", any(row["decision"] == "WEIGHTED_STOKES_IS_THE_CORRECT_LOCAL_BOUND_LAW" for row in decisions), "decision ledger selects weighted Stokes fallback law", "P8_Y5_R2FR_3089_DECISION_LEDGER.csv"),
        ("VAL3089_18_next_target_selected", len(next_target) == 1 and next_target[0]["next_id"] == "NEXT3089_0_3090", "next target is selected", "P8_Y5_R2FR_3089_NEXT_TARGET.csv"),
        ("VAL3089_19_branch_copies_exist", all(path.exists() for path in branch_paths), "branch copy CSVs exist", "P8_Y5_R2FR_3089_BRANCH_COPIES.csv"),
        ("VAL3089_20_formalization_untouched", not any(FORMALIZATION.rglob("*3089*")) if FORMALIZATION.exists() else True, "no 3089 files exist under formalization-workbench", str(FORMALIZATION)),
        ("VAL3089_21_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ removed", str(PYCACHE)),
        ("VAL3089_22_doc_written", DOC.exists() and "weighted_stokes_bound_law_staged_nonclaim" in text(DOC), "checkpoint markdown is written with nonclaim verdict", str(DOC)),
    ]
    return with_meta(
        [
            {"validation_id": validation_id, "passed": passed, "requirement": requirement, "evidence": evidence}
            for validation_id, passed, requirement, evidence in checks
        ]
    )


def main() -> None:
    remove_pycache()
    for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
        path.parent.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    boundary = boundary_rows()
    projector = projector_rows()
    domain = domain_rows()
    stokes = stokes_rows()
    source_pack = source_pack_rows()
    routes = route_verdict_rows()
    bridge = bridge_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["boundary"], boundary)
    write_csv(OUTPUTS["projector"], projector)
    write_csv(OUTPUTS["domain"], domain)
    write_csv(OUTPUTS["stokes"], stokes)
    write_csv(OUTPUTS["source_pack"], source_pack)
    write_csv(OUTPUTS["route_verdicts"], routes)
    write_csv(OUTPUTS["bridge"], bridge)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    copy_map = {
        OUTPUTS["boundary"]: BRANCH_OUTPUTS["boundary_copy"],
        OUTPUTS["projector"]: BRANCH_OUTPUTS["projector_copy"],
        OUTPUTS["stokes"]: BRANCH_OUTPUTS["stokes_copy"],
        OUTPUTS["source_pack"]: BRANCH_OUTPUTS["source_pack_copy"],
        OUTPUTS["next"]: BRANCH_OUTPUTS["next_copy"],
    }
    for source, destination in copy_map.items():
        shutil.copyfile(source, destination)

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    validation = validate(generated_paths, branch_paths)
    write_doc(sources, boundary, projector, domain, stokes, source_pack, routes, bridge, gates, decisions, next_target, validation)
    validation = validate(generated_paths, branch_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, boundary, projector, domain, stokes, source_pack, routes, bridge, gates, decisions, next_target, validation)

    remove_pycache()
    validation = validate(generated_paths, branch_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, boundary, projector, domain, stokes, source_pack, routes, bridge, gates, decisions, next_target, validation)

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
