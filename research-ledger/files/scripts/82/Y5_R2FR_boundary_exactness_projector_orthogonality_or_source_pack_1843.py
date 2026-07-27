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
QUARANTINE = MICROSCOPE / "quarantine" / "1843"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1843-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1843_0_1842_next",
        "source_key": "1842_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1842_NEXT_TARGET.csv",
        "needles": ["NEXT1842_0_primary", "1843-Y5-R2FR-boundary-exactness"],
        "role": "1842 selects boundary exactness/projector orthogonality or source pack.",
    },
    {
        "source_id": "SRC1843_1_1842_validation",
        "source_key": "1842_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1842_VALIDATION.csv",
        "needles": ["VAL1842_OVERALL", "PASS"],
        "role": "confirms 1842 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1843_2_1842_owner_verdict",
        "source_key": "1842_owner_verdict",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1842_OWNER_CLAUSES.csv",
        "needles": ["LOC1842_8_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1842 owner map is explicit but does not close current MTS.",
    },
    {
        "source_id": "SRC1843_3_1019_exactness",
        "source_key": "1019_boundary_exactness",
        "source_path": RESIDUALS / "P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv",
        "needles": ["BE1019_6_verdict", "fail_current_claim"],
        "role": "1019 boundary exactness route and failure.",
    },
    {
        "source_id": "SRC1843_4_1019_projector",
        "source_key": "1019_projector_orthogonality",
        "source_path": RESIDUALS / "P8_Y5_R10_1019_PROJECTOR_ORTHOGONALITY_CLAUSES.csv",
        "needles": ["PO1019_5_verdict", "fail_current_claim"],
        "role": "1019 projector orthogonality route and failure.",
    },
    {
        "source_id": "SRC1843_5_1019_source_pack",
        "source_key": "1019_source_pack_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv",
        "needles": ["SP1019_7_total_guard", "NOT_COMPUTED_COMPONENTS_MISSING"],
        "role": "1019 source pack schema for FB5540/bulk/edge/R11 no-cancellation guard.",
    },
    {
        "source_id": "SRC1843_6_1020_domain",
        "source_key": "1020_boundary_domain_certificate",
        "source_path": RESIDUALS / "P8_Y5_R10_1020_BOUNDARY_DOMAIN_CERTIFICATE.csv",
        "needles": ["BDC1020_5_verdict", "fail_current_claim"],
        "role": "1020 boundary domain/cohomology certificate and current blocker.",
    },
    {
        "source_id": "SRC1843_7_1020_stokes",
        "source_key": "1020_weighted_stokes",
        "source_path": RESIDUALS / "P8_Y5_R10_1020_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv",
        "needles": ["ETB1020_5_verdict", "fail_current_claim_but_derivation_progress"],
        "role": "1020 weighted-Stokes theorem and fallback bound.",
    },
    {
        "source_id": "SRC1843_8_1020_BX",
        "source_key": "1020_BX_primitive_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1020_BX_PRIMITIVE_AUDIT.csv",
        "needles": ["BXP1020_4_verdict", "fail_current_claim"],
        "role": "1020 identifies explicit B_X primitive as next hard object.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_SOURCE_REGISTER.csv",
    "boundary_exactness": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_BOUNDARY_EXACTNESS_CLAUSES.csv",
    "projector_orthogonality": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_PROJECTOR_ORTHOGONALITY_CLAUSES.csv",
    "domain_certificate": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_BOUNDARY_DOMAIN_CERTIFICATE.csv",
    "weighted_stokes": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv",
    "source_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_SOURCE_PACK_SCHEMA.csv",
    "route_verdicts": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_ROUTE_VERDICTS.csv",
    "gr_bridge": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_GR_BRIDGE_STATUS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1843_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def boundary_exactness_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BE1843_0_domain",
            "claim": "edge integration domain has no untracked corner or domain dependence",
            "mathematical_form": "partial S_edge=empty, or every corner C carries explicit Q_C in source pack",
            "current_status": "NOT_SIGNED",
            "what_would_close": "parent boundary class fixes S_edge and corner terms before readout",
            "failure_mode": "Stokes zero hides corner/domain charge",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BE1843_1_exact_BX",
            "claim": "boundary momentum is exact on the certified boundary class",
            "mathematical_form": "B_X=d_S b_X with no residual r_X and no harmonic h_X",
            "current_status": "NOT_DERIVED",
            "what_would_close": "derive b_X from parent L_X/Theta_X/Q_X plus fixed counterterm",
            "failure_mode": "Q_edge remains live or must be bounded",
            "valid_for_claim": False,
        },
        {
            "branch_id": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428",
            "clause_id": "BE1843_2_harmonic_residual",
            "claim": "no harmonic or residual edge class survives",
            "mathematical_form": "B_X=d_S b_X+h_X+r_X with h_X=r_X=0",
            "current_status": "NOT_SIGNED",
            "what_would_close": "boundary cohomology/no-hair theorem or source-backed h_X/r_X bounds",
            "failure_mode": "closed but wrong edge mode feeds R10/R11",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BE1843_3_closed_weight",
            "claim": "weighted Stokes derivative term vanishes",
            "mathematical_form": "d_S(F_lambda epsilon_X)=0 on S_edge",
            "current_status": "NOT_SIGNED",
            "what_would_close": "kernel/gauge weight closure theorem or source-backed derivative norm",
            "failure_mode": "exact B_X still leaves weighted derivative residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BE1843_4_counterterm_reference",
            "claim": "boundary counterterm/reference cannot be tuned after readout",
            "mathematical_form": "B_ct,B_ref fixed once; partial_source Delta_ref=0",
            "current_status": "NOT_SIGNED",
            "what_would_close": "parent variational principle fixes counterterm and reference class",
            "failure_mode": "reference absorbs source calibration or edge charge",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BE1843_5_verdict",
            "claim": "boundary exactness kills edge branch",
            "mathematical_form": "BE1843_0 through BE1843_4 imply Q_edge^H(lambda)=0 and K_boundary=0",
            "current_status": "FAIL_CURRENT_CLAIM",
            "what_would_close": "all exactness clauses parent-signed in one boundary class",
            "failure_mode": "retain source-pack fallback rows for Qbar_edge_XH and K_edge",
            "valid_for_claim": False,
        },
    ]


def projector_orthogonality_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PO1843_0_projector_definition",
            "claim": "Pi_M^H is the fixed Hamiltonian source-mass projector",
            "mathematical_form": "Pi_M^H[J] = component of J paired with same-frame M_H_ref",
            "current_status": "NOT_SIGNED",
            "what_would_close": "M_H_ref and Pi_M^H defined from parent Hamiltonian charge before readout",
            "failure_mode": "projector can select wrong object",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PO1843_1_edge_mass_independence",
            "claim": "edge charge has no same-frame source-mass dependence",
            "mathematical_form": "partial Q_edge^H(lambda)/partial M_H_ref |_{tau,reference,surface}=0",
            "current_status": "NOT_DERIVED",
            "what_would_close": "Q_edge depends only on fixed boundary cohomology/gauge data, not source worldtube data",
            "failure_mode": "Qbar_edge_XH(lambda) remains live",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PO1843_2_symplectic_block",
            "claim": "source and edge sectors are symplectically orthogonal",
            "mathematical_form": "Omega(delta_M Phi,delta_edge Phi)=0 and Pi_M^H[delta_edge Q]=0",
            "current_status": "NOT_DERIVED",
            "what_would_close": "block-diagonal reduced symplectic form or exact mixed term",
            "failure_mode": "edge/source mixing feeds FB5540 or R10/R11",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PO1843_3_reference_silence",
            "claim": "reference subtraction does not reroute edge charge into mass readout",
            "mathematical_form": "Pi_M^H[Delta_ref+Delta_symp+B_class]=0",
            "current_status": "NOT_SIGNED",
            "what_would_close": "B_ref derivative-silent theorem plus boundary class certificate",
            "failure_mode": "projector orthogonality broken by reference movement",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PO1843_4_conditional_zero",
            "claim": "projector clauses kill edge Hamiltonian source charge",
            "mathematical_form": "PO1843_0 through PO1843_3 imply Qbar_edge_XH(lambda)=0",
            "current_status": "CONDITIONAL_THEOREM_ONLY",
            "what_would_close": "parent-signed projector definition, mass-independence, block and reference lemmas",
            "failure_mode": "cannot zero edge projection row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PO1843_5_verdict",
            "claim": "projector orthogonality kills edge source projection",
            "mathematical_form": "Pi_M^H[Q_edge]=0 with no reference, tau, or surface leakage",
            "current_status": "FAIL_CURRENT_CLAIM",
            "what_would_close": "PO1843_0 through PO1843_4 signed by same parent action/boundary class",
            "failure_mode": "retain Qbar_edge_XH source-pack row",
            "valid_for_claim": False,
        },
    ]


def domain_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "BDC1843_0_surface_manifold",
            "object": "edge surface S_edge",
            "required_certificate": "compact oriented smooth codim-2 surface with no active corner boundary",
            "mathematical_test": "partial S_edge=empty or every corner C has explicit corner charge Q_C",
            "current_status": "NOT_SIGNED",
            "failure_if_missing": "Stokes zero can hide corner charge",
            "feeds": "Q_edge_zero;corner_source_row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "BDC1843_1_boundary_class",
            "object": "allowed boundary class B_class",
            "required_certificate": "same B_class used by L_X,Q_X,B_ref,Pi_M^H and R10/R11 readout",
            "mathematical_test": "delta B_class=0 along source variation and no retuning between source/test systems",
            "current_status": "NOT_SIGNED",
            "failure_if_missing": "reference or boundary class can absorb the signal",
            "feeds": "FB5540;Qbar_edge_XH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "BDC1843_2_relative_cohomology",
            "object": "relative edge cohomology H_edge",
            "required_certificate": "harmonic/non-exact edge class absent or separately measured as h_X",
            "mathematical_test": "B_X=d_S b_X+h_X with h_X=0, or |int_S F_lambda epsilon h_X| source-bounded",
            "current_status": "NOT_SIGNED",
            "failure_if_missing": "exactness misses a harmonic edge mode",
            "feeds": "harmonic_edge_bound;Q_edge_zero",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "BDC1843_3_allowed_epsilon",
            "object": "epsilon_X domain",
            "required_certificate": "epsilon_X is a proper X-representative gauge while physical tau/mass/rotation generators remain admissible",
            "mathematical_test": "epsilon_X|S_edge=0 or d_S(F_lambda epsilon_X)=0 without constraining tau_source or ADM charges",
            "current_status": "CLOSURE_ONLY",
            "failure_if_missing": "proper-gauge zero may erase real physical charges",
            "feeds": "Q_edge_zero;projector_definition",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "BDC1843_4_kernel_weight",
            "object": "F_lambda epsilon_X",
            "required_certificate": "edge kernel/gauge weight closed on S_edge or derivative term source-bounded",
            "mathematical_test": "d_S(F_lambda epsilon_X)=0, or ||d_S(F_lambda epsilon_X)||_* and ||b_X||_* are supplied",
            "current_status": "NOT_SIGNED",
            "failure_if_missing": "weighted Stokes identity leaves derivative residual",
            "feeds": "kernel_derivative_bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "BDC1843_5_verdict",
            "object": "boundary domain certificate",
            "required_certificate": "BDC1843_0 through BDC1843_4 signed in one parent boundary class",
            "mathematical_test": "closed/corner-free plus cohomology plus epsilon/kernel conditions imply no untracked edge domain term",
            "current_status": "FAIL_CURRENT_CLAIM",
            "failure_if_missing": "Q_edge cannot be set to zero by Stokes alone",
            "feeds": "1844_BX_primitive_or_edge_bound",
            "valid_for_claim": False,
        },
    ]


def weighted_stokes_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ETB1843_0_decomposition",
            "statement": "boundary momentum decomposes into exact, harmonic and residual pieces",
            "formula": "B_X=d_S b_X+h_X+r_X",
            "current_result": "FORMAL_DECOMPOSITION",
            "missing_for_claim": "parent L_X/Theta_X/Q_X must prove r_X=0 and identify h_X",
            "bound_if_missing": "|Q_edge| keeps |int_S F epsilon h_X| + |int_S F epsilon r_X|",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ETB1843_1_weighted_Stokes_identity",
            "statement": "exactness kills edge charge only when kernel/gauge weight has no surface derivative term",
            "formula": "int_S F epsilon d_S b_X = int_partialS F epsilon b_X - int_S d_S(F epsilon) wedge b_X",
            "current_result": "MATH_IDENTITY_WRITTEN",
            "missing_for_claim": "partialS=empty or corner row, plus d_S(F epsilon)=0 or a derivative bound",
            "bound_if_missing": "|int_S F epsilon d_S b_X| <= ||d_S(F epsilon)||_* ||b_X||_* + |corner_term|",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ETB1843_2_zero_conditions",
            "statement": "genuine edge-zero theorem needs exactness, no harmonic/residual/corner terms, and closed weight",
            "formula": "partialS=empty, h_X=0, r_X=0, d_S(F epsilon)=0 => Q_edge^H(lambda)=0",
            "current_result": "CONDITIONAL_THEOREM",
            "missing_for_claim": "all hypotheses unsigned in current MTS",
            "bound_if_missing": "use ETB1843_3 residual bound instead of zero",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ETB1843_3_residual_bound",
            "statement": "if exact zero fails, edge charge has a finite source-pack bound",
            "formula": "|Q_edge(lambda)| <= C_corner + ||d_S(F_lambda epsilon_X)||_* ||b_X||_* + |int_S F_lambda epsilon_X h_X| + |int_S F_lambda epsilon_X r_X|",
            "current_result": "BOUND_LAW_STAGED",
            "missing_for_claim": "numeric/source-backed norms for each term and units",
            "bound_if_missing": "first nonclaim source row stores terms with valid_for_claim=false",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ETB1843_4_projector_bound",
            "statement": "Hamiltonian/source projection is bounded after M_H_ref and Pi_M norm are owned",
            "formula": "|Qbar_edge_XH(lambda)| <= ||Pi_M^H|| |Q_edge(lambda)| / M_H_ref_min",
            "current_result": "CONDITIONAL_BOUND",
            "missing_for_claim": "Pi_M^H definition, M_H_ref_min and source-backed Q_edge bound",
            "bound_if_missing": "Qbar_edge_XH remains MISSING_SOURCE_BACKED_QBAR_EDGE_XH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ETB1843_5_verdict",
            "statement": "exact local condition and fallback bound are derived, but not the zero theorem",
            "formula": "Q_edge=0 conditional; Q_edge_bound schema-ready; no claim promoted",
            "current_result": "FAIL_CURRENT_CLAIM_BUT_DERIVATION_PROGRESS",
            "missing_for_claim": "B_X primitive, h_X/r_X zero or bounds, kernel derivative bound, corner audit, M_H_ref/Pi_M",
            "bound_if_missing": "move to 1844 B_X primitive or first source-bound term",
            "valid_for_claim": False,
        },
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "pack_id": "SP1843_0_M_H_ref",
            "quantity": "M_H_ref",
            "definition": "same-frame Hamiltonian source denominator",
            "required_columns": "system_id;tau_id;surface;Q_tau_integral;G_ref;H_ref;M_H_ref;units;reference_rule;source_path;valid_for_claim",
            "current_status": "MISSING_STABLE_MH_REF",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "SP1843_1_FB5540_components",
            "quantity": "delta_H_tau_nonintegrable_over_MH;Delta_ref_over_MH;symplectic_boundary_flux_over_MH",
            "definition": "componentwise FB5540 numerator rows normalized by M_H_ref",
            "required_columns": "system_id;component_id;value_abs;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_FB5540_COMPONENT_VALUES",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "SP1843_2_edge_bound_terms",
            "quantity": "C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs",
            "definition": "weighted-Stokes bound terms for Q_edge(lambda)",
            "required_columns": "system_id;lambda;C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs;units;source_path;valid_for_claim",
            "current_status": "MISSING_EDGEBOUND_TERMS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "SP1843_3_projected_edge_bound",
            "quantity": "Qbar_edge_XH_bound(lambda)",
            "definition": "projected edge bound after Pi_M^H norm and M_H_ref_min",
            "required_columns": "system_id;lambda;PiM_norm;Q_edge_bound;M_H_ref_min;Qbar_edge_XH_bound;units;source_path;valid_for_claim",
            "current_status": "MISSING_PIM_NORM_OR_MHREF_MIN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "SP1843_4_bulk_X_coefficients",
            "quantity": "Z_X;M_X2;J_X;lambda_X;K_X;Qbar_XH;qbar_XT",
            "definition": "bulk X residual coefficients if no-pole/source-free theorem fails",
            "required_columns": "system_id;field_id;Z_X;M_X2;J_X;lambda_X;K_X;Qbar_XH;qbar_XT;units;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_INPUT_OR_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "SP1843_5_edge_coefficients",
            "quantity": "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge(lambda)",
            "definition": "edge residual amplitude if boundary/projector theorem fails",
            "required_columns": "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge;units;source_path;valid_for_claim",
            "current_status": "MISSING_EDGE_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "SP1843_6_total_guard",
            "quantity": "alpha_total_guard(lambda)",
            "definition": "absolute no-cancellation envelope across FB5540, bulk X, edge X and R11",
            "required_columns": "system_id;lambda;abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_alpha_R11;component_sum_abs;bound;source_path;valid_for_claim",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "valid_for_claim": False,
        },
    ]


def route_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "RVT1843_0_boundary_exactness",
            "route": "derive Q_edge=0 from exact boundary form",
            "status": "CONDITIONAL_NOT_PROMOTED",
            "requires": "BE1843 clauses plus BDC1843 certificates and ETB1843 zero conditions",
            "result": "FAIL_CURRENT_CLAIM",
            "fallback": "retain edge source-pack rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RVT1843_1_projector_orthogonality",
            "route": "derive Qbar_edge_XH=0 from mass-projector orthogonality",
            "status": "CONDITIONAL_NOT_PROMOTED",
            "requires": "PO1843 clauses plus M_H_ref/Pi_M^H owner",
            "result": "FAIL_CURRENT_CLAIM",
            "fallback": "source or bound Pi_M^H[Q_edge]",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RVT1843_2_weighted_stokes_bound",
            "route": "finite edge residual bound from derivative/harmonic/corner terms",
            "status": "BEST_CURRENT_FALLBACK",
            "requires": "C_corner,norm_dS_Feps,norm_bX,harmonic_edge_abs,residual_edge_abs,M_H_ref_min,PiM_norm",
            "result": "SOURCE_PACK_SCHEMA_READY_NO_VALUES",
            "fallback": "1844 B_X primitive or first edge-bound term",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RVT1843_3_no_double_count",
            "route": "orthogonal source split prevents duplicate scoring",
            "status": "GUARD_WRITTEN_NOT_DERIVED",
            "requires": "bulk/edge/FB5540/R11 projectors and source currents",
            "result": "BLOCKS_CURRENT_CLAIM",
            "fallback": "absolute no-cancellation envelope",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RVT1843_4_verdict",
            "route": "1843 branch closure",
            "status": "FAIL_CURRENT_CLAIM_BUT_NARROWS_GAP",
            "requires": "theorem-zero route or complete source pack",
            "result": "no R10/R11/Newton/local-GR pass",
            "fallback": "1844 explicit B_X primitive from parent variation or edge-bound term fill",
            "valid_for_claim": False,
        },
    ]


def gr_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1843_0_edge_zero",
            "bridge_piece": "edge/boundary zero theorem",
            "current_status": "CONDITIONAL_NOT_PROMOTED",
            "evidence": "BE1843;BDC1843;ETB1843",
            "remaining_gap": "B_X primitive, cohomology, corner, kernel-weight and reference certificates missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1843_1_projector_zero",
            "bridge_piece": "edge-source projector orthogonality",
            "current_status": "CONDITIONAL_NOT_PROMOTED",
            "evidence": "PO1843",
            "remaining_gap": "Pi_M^H, M_H_ref, source/edge symplectic block and reference silence unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1843_2_source_pack",
            "bridge_piece": "FB5540/bulk/edge/R11 source pack",
            "current_status": "SCHEMA_READY_NO_VALUES",
            "evidence": "SP1843 rows",
            "remaining_gap": "all source-backed numeric/theorem-zero terms missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1843_3_Newton_GR",
            "bridge_piece": "Newton/local-GR bridge",
            "current_status": "BLOCKED",
            "evidence": "RVT1843_4",
            "remaining_gap": "edge/source leakage and M_H_ref normalization still open",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1843_4_next",
            "bridge_piece": "next derivation owner",
            "current_status": "BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_IS_NEXT",
            "evidence": "ETB1843_5;1020 B_X primitive audit",
            "remaining_gap": "derive explicit b_X primitive or fill first weighted-Stokes bound term",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1843_0_boundary_exactness_closed",
            "claim": "boundary exactness theorem closes Q_edge",
            "gate_pass": False,
            "reason": "domain, B_X primitive, harmonic/residual, kernel-weight and reference clauses are unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1843_1_projector_orthogonality_closed",
            "claim": "projector orthogonality theorem closes Qbar_edge_XH",
            "gate_pass": False,
            "reason": "Pi_M^H definition, edge mass-independence, symplectic block and reference silence are unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1843_2_weighted_stokes_zero",
            "claim": "weighted Stokes gives Q_edge=0",
            "gate_pass": False,
            "reason": "d_S(F_lambda epsilon_X)=0, h_X=r_X=0 and no-corner conditions are not proved",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1843_3_source_pack_complete",
            "claim": "FB5540/bulk/edge/R11 source pack is complete",
            "gate_pass": False,
            "reason": "source pack rows remain missing or not computed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1843_4_first_bound_rows_staged",
            "claim": "first edge bound row schema is staged as nonclaim",
            "gate_pass": True,
            "reason": "weighted-Stokes bound terms are explicit but missing source values",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1843_5_R10_R11_Newton_GR",
            "claim": "R10/R11/Newton/local-GR can pass",
            "gate_pass": False,
            "reason": "no theorem-zero or complete source-backed comparator row exists",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1843_0_theorem_attempt",
            "decision": "BOUNDARY_PROJECTOR_ROUTE_PRECISE_BUT_NOT_CLOSED",
            "reason": "Stokes/projector arguments can kill edge leakage only after boundary domain, B_X primitive, cohomology, kernel and reference clauses are parent-signed",
            "next_action": "derive explicit B_X primitive from parent variation or fill bound terms",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1843_1_weighted_stokes",
            "decision": "WEIGHTED_STOKES_IS_THE_CORRECT_LOCAL_BOUND_LAW",
            "reason": "exactness alone is insufficient when F_lambda epsilon_X has a surface derivative, harmonic piece, residual piece, or corner term",
            "next_action": "carry C_corner, norm_dS_Feps, norm_bX, harmonic_edge_abs and residual_edge_abs explicitly",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1843_2_source_pack",
            "decision": "NO_CANCELLATION_SOURCE_PACK_REQUIRED_IF_THEOREM_FAILS",
            "reason": "edge, bulk, FB5540 and R11 components cannot cancel while inputs are unknown",
            "next_action": "do not run comparators until source pack terms are real",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1843_3_best_next",
            "decision": "BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_IS_NEXT",
            "reason": "without b_X, both the zero theorem and weighted-Stokes bound lack their central object",
            "next_action": "1844-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1843_0_primary",
            "next_target": "1844-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
            "script": "scripts/Y5_R2FR_BX_primitive_from_parent_variation_or_edge_bound_term_fill_1844.py",
            "objective": "derive the explicit B_X primitive from parent L_X/Theta_X/Q_X and boundary counterterm, or fill the first EDGEBOUND term with source-backed units",
            "selection_status": "selected",
            "success_condition": "b_X is derived with boundary/cohomology certificates, or C_corner/norm_dS_Feps/norm_bX/harmonic/residual terms are source-backed nonclaim rows",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1843_1_parallel",
            "next_target": "1844b-Y5-R2FR-MHref-PiM-norm-edge-bound-acquisition.md",
            "script": "scripts/Y5_R2FR_MHref_PiM_norm_edge_bound_acquisition_1844b.py",
            "objective": "stage M_H_ref_min and Pi_M^H norm inputs needed to project Q_edge_bound to Qbar_edge_XH_bound",
            "selection_status": "parallel_held",
            "success_condition": "projected edge bound remains nonclaim until denominator, projector norm and edge bound are all source-backed",
        },
    ]


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "boundary_exactness": boundary_exactness_rows(),
        "projector_orthogonality": projector_orthogonality_rows(),
        "domain_certificate": domain_certificate_rows(),
        "weighted_stokes": weighted_stokes_rows(),
        "source_pack": source_pack_rows(),
        "route_verdicts": route_verdict_rows(),
        "gr_bridge": gr_bridge_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames(rows: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    for row in rows:
        for key in row:
            if key not in names:
                names.append(key)
    return names


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames(rows))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        for target in [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1843_{key.upper()}.csv",
        ]:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1843_{key.upper()}.csv").exists():
            return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = [
        "1843-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1843",
        "P8_Y5_BRR545_1843",
        "Y5_R2FR_boundary_exactness_projector_orthogonality_or_source_pack_1843",
    ]
    return not any(any(marker in path.name for marker in markers) for path in FORMALIZATION.rglob("*"))


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    allowed_true = {"CG1843_4_first_bound_rows_staged"}
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            if row.get("gate_id") in allowed_true and row.get("gate_pass") is True:
                continue
            for field in ["valid_for_claim", "claim_allowed", "gate_pass", "score_ready"]:
                if row.get(field) is True:
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            has_missing = any("MISSING_" in str(value) for value in row.values())
            if not has_missing:
                continue
            for field in ["valid_for_claim", "claim_allowed", "score_ready"]:
                if row.get(field) is True:
                    return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    checks = [
        ("VAL1843_0_sources_exist", all(row["exists"] is True for row in source_rows), "all cited source paths exist"),
        ("VAL1843_1_needles_present", all(row["needles_present"] is True for row in source_rows), "all cited source needles are present"),
        (
            "VAL1843_2_exactness_blocks_claim",
            any(row["clause_id"] == "BE1843_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["boundary_exactness"]),
            "boundary exactness theorem remains nonclaim",
        ),
        (
            "VAL1843_3_projector_blocks_claim",
            any(row["clause_id"] == "PO1843_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["projector_orthogonality"]),
            "projector orthogonality theorem remains nonclaim",
        ),
        (
            "VAL1843_4_domain_certificate_complete",
            {"BDC1843_0_surface_manifold", "BDC1843_2_relative_cohomology", "BDC1843_4_kernel_weight", "BDC1843_5_verdict"}.issubset({row["certificate_id"] for row in rows_map["domain_certificate"]}),
            "domain certificate covers surface, cohomology, kernel and verdict",
        ),
        (
            "VAL1843_5_weighted_stokes_written",
            any(row["theorem_id"] == "ETB1843_5_verdict" and row["current_result"] == "FAIL_CURRENT_CLAIM_BUT_DERIVATION_PROGRESS" for row in rows_map["weighted_stokes"]),
            "weighted-Stokes theorem and fallback bound are written",
        ),
        (
            "VAL1843_6_source_pack_nonclaim",
            {"SP1843_0_M_H_ref", "SP1843_2_edge_bound_terms", "SP1843_6_total_guard"}.issubset({row["pack_id"] for row in rows_map["source_pack"]})
            and all(row["valid_for_claim"] is False for row in rows_map["source_pack"]),
            "source pack rows are explicit and nonclaim",
        ),
        (
            "VAL1843_7_bridge_next",
            any(row["status_id"] == "GB1843_4_next" and row["current_status"] == "BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_IS_NEXT" for row in rows_map["gr_bridge"]),
            "bridge status selects B_X primitive/edge-bound next",
        ),
        (
            "VAL1843_8_claim_gates_blocked",
            all((row["gate_pass"] is False or row["gate_id"] == "CG1843_4_first_bound_rows_staged") and row["claim_allowed"] is False for row in rows_map["claim_gate"]),
            "all claim gates remain blocked except nonclaim staging row",
        ),
        ("VAL1843_9_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1843_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1843_11_decision_next",
            any(row["decision_id"] == "DEC1843_3_best_next" and row["decision"] == "BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_IS_NEXT" for row in rows_map["decision"]),
            "decision selects B_X primitive or edge-bound fill",
        ),
        (
            "VAL1843_12_next_selected",
            any(row["route_id"] == "NEXT1843_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1843_13_csv_parse", csv_parse_all(), "all generated 1843 CSVs parse"),
        ("VAL1843_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1843_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1843_16_formalization_untouched", no_formalization_outputs(), "no 1843 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1843_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1843 boundary exactness projector orthogonality or source pack",
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
            "# 1843 Y5 R2FR boundary exactness projector orthogonality or source pack",
            "",
            "**Progress:** 1843 turns the edge/source leakage problem into exact local conditions: certified boundary domain, explicit `B_X=d_S b_X+h_X+r_X`, closed weighted-Stokes kernel, projector orthogonality, and a no-cancellation source pack if any theorem route fails.",
            "",
            "**Current verdict:** no boundary-zero or projector-zero claim is allowed. The useful progress is that `Q_edge=0` now has exact conditions, and if those conditions fail the fallback is a finite weighted-Stokes bound, not a closure axiom.",
            "",
            "**Claim ceiling:** no `Q_edge=0`, `Qbar_edge_XH=0`, R10/R11 pass, Newton/local-GR reduction, PPN pass, edge-source cancellation, GitHub action, or `formalization-workbench` edit is allowed from 1843.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Boundary Exactness Clauses",
            markdown_table(rows_map["boundary_exactness"], ["clause_id", "claim", "mathematical_form", "current_status", "what_would_close", "failure_mode", "valid_for_claim"]),
            "",
            "## Projector Orthogonality Clauses",
            markdown_table(rows_map["projector_orthogonality"], ["clause_id", "claim", "mathematical_form", "current_status", "what_would_close", "failure_mode", "valid_for_claim"]),
            "",
            "## Boundary Domain Certificate",
            markdown_table(rows_map["domain_certificate"], ["certificate_id", "object", "required_certificate", "mathematical_test", "current_status", "failure_if_missing", "feeds", "valid_for_claim"]),
            "",
            "## Weighted Stokes Theorem And Bound",
            markdown_table(rows_map["weighted_stokes"], ["theorem_id", "statement", "formula", "current_result", "missing_for_claim", "bound_if_missing", "valid_for_claim"]),
            "",
            "## Source Pack Schema",
            markdown_table(rows_map["source_pack"], ["pack_id", "quantity", "definition", "required_columns", "current_status", "valid_for_claim"]),
            "",
            "## Route Verdicts",
            markdown_table(rows_map["route_verdicts"], ["route_id", "route", "status", "requires", "result", "fallback", "valid_for_claim"]),
            "",
            "## GR Bridge Status",
            markdown_table(rows_map["gr_bridge"], ["status_id", "bridge_piece", "current_status", "evidence", "remaining_gap", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is real progress toward a derivable GR/Newton bridge: the edge sector is no longer a vague 'boundary effect'. It is now an explicit weighted-Stokes problem. The next hard object is `b_X`; without it, both zero and bound routes are missing their central primitive.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1843 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
