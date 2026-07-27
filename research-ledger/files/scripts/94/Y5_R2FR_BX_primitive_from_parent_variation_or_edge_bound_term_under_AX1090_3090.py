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

CHECKPOINT = "3090"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3090-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-under-AX1090.md"

SOURCES = {
    "SRC3090_00_3089_doc": {
        "path": ROOT / "3089-Y5-R2FR-boundary-exactness-projector-orthogonality-or-FB5540-source-pack-under-AX1090.md",
        "needles": ["B_X=d_S b_X+h_X+r_X", "weighted-Stokes"],
        "role": "3089 derives the weighted-Stokes bound law and selects B_X primitive or edge-bound fill.",
    },
    "SRC3090_01_3089_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3089_NEXT_TARGET.csv",
        "needles": ["NEXT3089_0_3090", "B_X=d_S b_X+h_X+r_X"],
        "role": "3089 handoff names this B_X primitive / edge-bound target.",
    },
    "SRC3090_02_3089_stokes": {
        "path": RESIDUALS / "P8_Y5_R2FR_3089_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv",
        "needles": ["ETB3089_3_residual_bound", "BOUND_LAW_STAGED"],
        "role": "3089 source-backed local bound formula to inherit.",
    },
    "SRC3090_03_1844_precedent": {
        "path": ROOT / "1844-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
        "needles": ["explicit B_X primitive is still not derivable", "least-scrutiny route"],
        "role": "1844 precedent splits the B_X primitive, scalar no-hair and edge-bound routes.",
    },
    "SRC3090_04_1021_parent_template": {
        "path": RESIDUALS / "P8_Y5_R10_1021_PARENT_VARIATION_TEMPLATE.csv",
        "needles": ["PVT1021_5_verdict", "map_written_not_closed"],
        "role": "1021 parent variation to B_X primitive map.",
    },
    "SRC3090_05_1021_primitive_gates": {
        "path": RESIDUALS / "P8_Y5_R10_1021_BX_PRIMITIVE_GATES.csv",
        "needles": ["BXG1021_5_verdict", "fail_current_claim"],
        "role": "1021 primitive closure gates.",
    },
    "SRC3090_06_1021_scalar_split": {
        "path": RESIDUALS / "P8_Y5_R10_1021_SCALAR_BRANCH_SEPARATION.csv",
        "needles": ["SB1021_3_scalar_verdict", "separates_routes"],
        "role": "1021 scalar branch separation guardrail.",
    },
    "SRC3090_07_1021_edge_fill": {
        "path": RESIDUALS / "P8_Y5_R10_1021_EDGE_BOUND_FILL_SCHEMA.csv",
        "needles": ["EBF1021_5_verdict", "not_fillable_currently"],
        "role": "1021 first edge-bound fill schema.",
    },
    "SRC3090_08_1020_first_bound": {
        "path": RESIDUALS / "P8_Y5_R10_1020_SOURCE_PACK_FIRST_BOUND_ROW.csv",
        "needles": ["EDGEBOUND1020_0_formal_bound_row", "MISSING_BX_PRIMITIVE_NORM"],
        "role": "1020 formal first weighted-Stokes bound rows.",
    },
    "SRC3090_09_1021_next": {
        "path": RESIDUALS / "P8_Y5_R10_1021_NEXT_TARGET.csv",
        "needles": ["vertical-quotient-LX-construction", "scalar positive no-hair"],
        "role": "1021 selects vertical quotient versus scalar no-hair branch choice.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3090_SOURCE_REGISTER.csv",
    "parent_variation": RESIDUALS / "P8_Y5_R2FR_3090_PARENT_VARIATION_TEMPLATE.csv",
    "primitive_gates": RESIDUALS / "P8_Y5_R2FR_3090_BX_PRIMITIVE_GATES.csv",
    "branch_split": RESIDUALS / "P8_Y5_R2FR_3090_BRANCH_SEPARATION.csv",
    "edge_fill": RESIDUALS / "P8_Y5_R2FR_3090_EDGE_BOUND_FILL_SCHEMA.csv",
    "route_verdicts": RESIDUALS / "P8_Y5_R2FR_3090_ROUTE_VERDICTS.csv",
    "bridge": RESIDUALS / "P8_Y5_R2FR_3090_GR_BRIDGE_STATUS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3090_CLAIM_GATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3090_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3090_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3090_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3090_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "primitive_copy": LOCAL_BOUNDS / "BX_primitive_gates_3090_NONCLAIM.csv",
    "branch_split_copy": LOCAL_BOUNDS / "branch_separation_3090_NONCLAIM.csv",
    "edge_fill_copy": LOCAL_BOUNDS / "edge_bound_fill_schema_3090_NONCLAIM.csv",
    "bridge_copy": LOCAL_BOUNDS / "GR_bridge_status_3090_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3090_vertical_quotient_or_scalar_nohair_NEXT_NONCLAIM.csv",
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


def file_text(path: Path) -> str:
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
    base = metadata()
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


def source_register_rows() -> list[dict[str, Any]]:
    output_rows: list[dict[str, Any]] = []
    for source_id, source in SOURCES.items():
        path = Path(source["path"])
        content = file_text(path)
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


def parent_variation_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "template_id": "PVT3090_0_parent_first_variation",
                "object": "parent X-sector first variation",
                "formula": "delta L_X = E_A^X delta X^A + d Theta_X(Phi,delta X)",
                "closure_test": "L_X, field normalization, source coupling and boundary terms are all parent-signed before local readout",
                "current_status": "FORMULA_TRANSFERRED_NOT_PARENT_SIGNED",
                "implication": "variation algebra is available but not a derivation of the MTS edge primitive",
            },
            {
                "template_id": "PVT3090_1_vertical_Noether_route",
                "object": "vertical/gauge branch",
                "formula": "delta_epsilon X^A=R_i^A epsilon^i+R_i^{A mu} nabla_mu epsilon^i; J_epsilon=Theta_X(delta_epsilon X)-mu_epsilon=dQ_epsilon+epsilon C_X",
                "closure_test": "vertical generator is actual parent gauge direction and not a fitted local closure",
                "current_status": "VERTICAL_GENERATOR_UNSIGNED",
                "implication": "Noether edge silence cannot be claimed yet",
            },
            {
                "template_id": "PVT3090_2_boundary_covector",
                "object": "boundary adjoint covector",
                "formula": "B_DC[X,deltaY]=-int_S n_mu X_nu delta P^{mu nu}+delta Q_X+density/reference terms",
                "closure_test": "delta Q_X cancels every boundary covector or remaining covectors are explicitly bounded",
                "current_status": "COVECTOR_OWNER_MISSING",
                "implication": "edge source cannot be zeroed by exactness words without a primitive",
            },
            {
                "template_id": "PVT3090_3_BX_definition",
                "object": "edge boundary momentum",
                "formula": "B_X := i_S^*(n_mu P_X^{mu nu} epsilon_nu + B_ct[epsilon]) as a surface top form",
                "closure_test": "P_X and B_ct are fixed by the same parent action and reference principle",
                "current_status": "DEFINITION_WRITTEN_PRIMITIVE_NOT_DERIVED",
                "implication": "B_X is the current derivation bottleneck",
            },
            {
                "template_id": "PVT3090_4_hodge_decomposition",
                "object": "surface decomposition",
                "formula": "B_X=d_S b_X+h_X+r_X on S_edge",
                "closure_test": "derive b_X and show h_X=r_X=0, or source-bound all three terms",
                "current_status": "DECOMPOSITION_CONTRACT_READY",
                "implication": "weighted-Stokes bound has a precise algebraic slot but no source-backed payload",
            },
            {
                "template_id": "PVT3090_5_verdict",
                "object": "parent variation to primitive map",
                "formula": "parent L_X/Theta_X/Q_X -> P_X,B_ct -> B_X -> d_S b_X+h_X+r_X -> Q_edge bound",
                "closure_test": "every arrow is parent-signed or theorem-zero, with no missing edge-bound term",
                "current_status": "MAP_WRITTEN_NOT_CLOSED",
                "implication": "B_X primitive is not derived in current MTS",
            },
        ]
    )


def primitive_gate_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "gate_id": "BXG3090_0_same_parent_origin",
                "primitive_requirement": "P_X, J_X, Theta_X, Q_X, Omega_X and B_ct all come from one parent L_X",
                "test": "compare adjoint operator, Noether current, symplectic form and counterterm from the same action",
                "current_result": "FAIL_CURRENT_CLAIM",
                "missing_for_claim": "single signed parent sector action with source normalization and boundary reference",
                "if_missing": "B_X can be an assembled closure rather than a derived primitive",
            },
            {
                "gate_id": "BXG3090_1_counterterm_owner",
                "primitive_requirement": "B_ct is fixed before readout",
                "test": "delta(Q_X+B_ct)-i_epsilon Theta_X has no uncancelled boundary covector",
                "current_result": "NOT_DERIVED",
                "missing_for_claim": "differentiability/reference principle for the X-sector boundary class",
                "if_missing": "reference/counterterm can accidentally absorb source calibration",
            },
            {
                "gate_id": "BXG3090_2_exact_surface_pullback",
                "primitive_requirement": "i_S^*B_X-h_X is exact on S_edge",
                "test": "construct b_X with B_X-h_X=d_S b_X and verify patch overlap compatibility",
                "current_result": "NOT_DERIVED",
                "missing_for_claim": "explicit b_X primitive or theorem bounding norm_bX",
                "if_missing": "weighted-Stokes exact route remains conditional",
            },
            {
                "gate_id": "BXG3090_3_harmonic_zero",
                "primitive_requirement": "harmonic/cohomology edge class vanishes or is bounded",
                "test": "Pi_Hedge[B_X]=0, or h_X coefficient bound is source-backed",
                "current_result": "MISSING_COHOMOLOGY_PROOF_OR_BOUND",
                "missing_for_claim": "boundary cohomology certificate plus source-backed harmonic bound",
                "if_missing": "closed edge classes can feed R10/R11",
            },
            {
                "gate_id": "BXG3090_4_kernel_norm",
                "primitive_requirement": "d_S(F_lambda epsilon_X) is zero or bounded",
                "test": "closed weight on S_edge, or source-backed norm_dS_Feps",
                "current_result": "MISSING_KERNEL_DERIVATIVE_BOUND",
                "missing_for_claim": "edge geometry, lambda support and allowed epsilon_X domain",
                "if_missing": "even exact B_X leaves a weighted derivative residual",
            },
            {
                "gate_id": "BXG3090_5_verdict",
                "primitive_requirement": "B_X primitive closure",
                "test": "BXG3090_0 through BXG3090_4 close together",
                "current_result": "FAIL_CURRENT_CLAIM",
                "missing_for_claim": "parent-signed primitive or source-backed edge-bound pack",
                "if_missing": "move to vertical quotient construction or scalar/source coefficient fallback",
            },
        ]
    )


def branch_split_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "branch_id": "BRS3090_0_vertical_quotient",
                "branch": "construct X as absent/vertical quotient before variation",
                "formula": "q(Phi+epsilon v_X)=q(Phi), Dq[v_X]=0, S_parent descends and Q_edge[v_X]=0",
                "status": "BEST_LEAST_SCRUTINY_ROUTE_NOT_CLOSED",
                "why": "removing the local pole before variation is cleaner than bounding a leftover coupling",
                "next_test": "q map, v_X, action descent, matter descent, boundary silence and degree count close together",
            },
            {
                "branch_id": "BRS3090_1_Noether_edge_primitive",
                "branch": "derive B_X as a Noether/vertical primitive",
                "formula": "J_epsilon=dQ_epsilon+epsilon C_X and i_S^*B_X=d_S b_X+h_X+r_X",
                "status": "NOT_CLOSED",
                "why": "requires same parent L_X/Theta_X/Q_X/Omega_X/B_ct owner",
                "next_test": "prove B_X primitive or retain weighted-Stokes source terms",
            },
            {
                "branch_id": "BRS3090_2_scalar_nohair",
                "branch": "positive scalar/source-free no-hair",
                "formula": "O_X X=-nabla_i(Z_X nabla^i X)+M_X^2X=J_X with Z_X>0,M_X^2>=0,J_X=0",
                "status": "SEPARATE_FALLBACK_NOT_EDGE_PROOF",
                "why": "can silence X under signed positivity/source-free boundary data but does not prove Q_edge exactness",
                "next_test": "source Z_X, M_X2, J_X and parent-selected boundary conditions",
            },
            {
                "branch_id": "BRS3090_3_edge_bound",
                "branch": "finite weighted-Stokes edge residual",
                "formula": "Q_edge_bound=C_corner+norm_dS_Feps*norm_bX+harmonic_edge_abs+residual_edge_abs",
                "status": "FALLBACK_SCHEMA_READY_VALUES_MISSING",
                "why": "keeps theory testable if theorem-zero routes fail",
                "next_test": "fill edge-bound rows as source-backed nonclaim inputs",
            },
            {
                "branch_id": "BRS3090_4_route_guardrail",
                "branch": "do not mix proof languages",
                "formula": "vertical quotient != scalar no-hair != edge-bound residual",
                "status": "GUARDRAIL_INSTALLED",
                "why": "prevents a scalar boundary condition from being sold as a Noether edge-zero theorem",
                "next_test": "select one branch per claim and keep all fallback rows nonclaim",
            },
        ]
    )


def edge_fill_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "fill_id": "EBF3090_0_norm_bX",
                "quantity": "norm_bX",
                "definition": "dual norm of the primitive b_X entering |int_S d_S(F epsilon) wedge b_X|",
                "required_source": "explicit b_X from P_X/B_ct or a theorem-bound on b_X",
                "current_status": "MISSING_BX_PRIMITIVE_OR_BOUND",
                "units": "MISSING_EDGE_PRIMITIVE_UNITS",
                "source_path": "MISSING_SOURCE_PATH",
            },
            {
                "fill_id": "EBF3090_1_harmonic_edge_abs",
                "quantity": "harmonic_edge_abs",
                "definition": "absolute harmonic/cohomology contribution |int_S F epsilon h_X|",
                "required_source": "H_edge projection of B_X or no-hair/cohomology theorem",
                "current_status": "MISSING_H_EDGE_ZERO_OR_BOUND",
                "units": "MISSING_EDGE_CHARGE_UNITS",
                "source_path": "MISSING_SOURCE_PATH",
            },
            {
                "fill_id": "EBF3090_2_residual_edge_abs",
                "quantity": "residual_edge_abs",
                "definition": "absolute non-exact/non-harmonic residual contribution |int_S F epsilon r_X|",
                "required_source": "proof r_X=0 or a source-backed residual bound",
                "current_status": "MISSING_PARENT_RESIDUAL_BOUND",
                "units": "MISSING_EDGE_CHARGE_UNITS",
                "source_path": "MISSING_SOURCE_PATH",
            },
            {
                "fill_id": "EBF3090_3_norm_dS_Feps",
                "quantity": "norm_dS_Feps",
                "definition": "surface derivative norm of F_lambda epsilon_X over the selected edge geometry",
                "required_source": "edge geometry, lambda support and allowed epsilon_X domain",
                "current_status": "MISSING_KERNEL_DERIVATIVE_BOUND",
                "units": "MISSING_INVERSE_LENGTH_OR_DUAL_UNITS",
                "source_path": "MISSING_SOURCE_PATH",
            },
            {
                "fill_id": "EBF3090_4_corner",
                "quantity": "C_corner",
                "definition": "absolute corner contribution if the edge surface has a boundary or joints",
                "required_source": "corner-free certificate or corner charge bound",
                "current_status": "MISSING_CORNER_AUDIT",
                "units": "MISSING_EDGE_CHARGE_UNITS",
                "source_path": "MISSING_SOURCE_PATH",
            },
            {
                "fill_id": "EBF3090_5_verdict",
                "quantity": "EDGEBOUND fillability",
                "definition": "first executable edge-bound row requires all EBF3090_0 through EBF3090_4",
                "required_source": "primitive or numeric/source-backed bound for every term",
                "current_status": "NOT_FILLABLE_CURRENTLY",
                "units": "mixed_missing_units",
                "source_path": str(OUTPUTS["edge_fill"]),
            },
        ]
    )


def route_verdict_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "route_id": "R3090_0_vertical_quotient",
                "route": "construct X as absent/vertical quotient before variation",
                "status": "BEST_CLEAN_ROUTE_NOT_CLOSED",
                "because": "if X is genuine vertical redundancy, local source poles disappear before fitting",
                "next_step": "construct q, v_X, action descent, matter descent, boundary silence and degree count",
            },
            {
                "route_id": "R3090_1_BX_Noether_primitive",
                "route": "derive B_X as a Noether/vertical primitive",
                "status": "NOT_CLOSED",
                "because": "parent L_X/Theta_X/Q_X/P_X/B_ct chain remains contract-only",
                "next_step": "attempt vertical quotient construction instead of symbolic exactness",
            },
            {
                "route_id": "R3090_2_scalar_nohair",
                "route": "positive scalar/source-free no-hair",
                "status": "FALLBACK_SEPARATE_ROUTE",
                "because": "can yield X=0 under signed positivity and source-free boundary data, but is not an edge primitive",
                "next_step": "source Z_X,M_X2,J_X,boundary conditions and no-hair theorem if quotient route fails",
            },
            {
                "route_id": "R3090_3_edge_bound_fill",
                "route": "finite edge-bound residual",
                "status": "FALLBACK_SCHEMA_READY_VALUES_MISSING",
                "because": "weighted-Stokes gives a finite bound once b_X,harmonic,residual,kernel and corner terms are sourced",
                "next_step": "fill EDGEBOUND rows as nonclaim source-backed inputs if theorem routes fail",
            },
            {
                "route_id": "R3090_4_verdict",
                "route": "B_X primitive checkpoint",
                "status": "FAIL_CURRENT_CLAIM_BUT_SPLITS_ROUTES",
                "because": "primitive map is exact enough to audit but not parent-signed enough to claim",
                "next_step": "move to vertical quotient construction or scalar no-hair branch choice",
            },
        ]
    )


def bridge_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "status_id": "GB3090_0_BX_primitive",
                "bridge_piece": "edge primitive needed for local GR silence",
                "current_status": "BLOCKED_NOT_PARENT_SIGNED",
                "evidence": "PVT3090_5;BXG3090_5",
                "remaining_gap": "derive b_X from parent L_X/Theta_X/Q_X/B_ct or source-bound the edge terms",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3090_1_vertical_quotient",
                "bridge_piece": "remove X before local variation",
                "current_status": "BEST_NEXT_NOT_PROVED",
                "evidence": "BRS3090_0;R3090_0",
                "remaining_gap": "q, v_X, action descent, matter descent, boundary silence and degree count missing as one theorem",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3090_2_scalar_branch",
                "bridge_piece": "positive scalar no-hair local silence",
                "current_status": "SEPARATE_FALLBACK_NOT_EDGE_PROOF",
                "evidence": "BRS3090_2;R3090_2",
                "remaining_gap": "source Z_X/M_X2/J_X and parent-selected boundary conditions",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3090_3_edge_bound",
                "bridge_piece": "finite weighted-Stokes edge residual",
                "current_status": "SCHEMA_READY_VALUES_MISSING",
                "evidence": "EBF3090 rows",
                "remaining_gap": "fill norm_bX, harmonic/residual terms, kernel derivative and corner audit",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3090_4_local_GR_Newton",
                "bridge_piece": "derived local GR/Newton reduction",
                "current_status": "BLOCKED",
                "evidence": "R3090_4",
                "remaining_gap": "nonzero or unbounded edge/local source branch still possible",
                "bridge_claim": False,
            },
            {
                "status_id": "GB3090_5_next",
                "bridge_piece": "next derivation owner",
                "current_status": "VERTICAL_QUOTIENT_LX_CONSTRUCTION_OR_SCALAR_NOHAIR_BRANCH_CHOICE_IS_NEXT",
                "evidence": "DEC3090_2;NEXT3090_0",
                "remaining_gap": "choose/test least-scrutiny local branch without mixing routes",
                "bridge_claim": False,
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {"gate_id": "CG3090_0_sources_registered", "claim": "3090 source chain exists", "gate_pass": True, "reason": "sources exist for audit only; they do not make parent primitive signed", "claim_allowed_for_physics": False},
            {"gate_id": "CG3090_1_BX_primitive_derived", "claim": "B_X=d_S b_X+h_X+r_X is derived", "gate_pass": False, "reason": "PVT3090_5 and BXG3090_5 remain fail-current-claim", "claim_allowed_for_physics": False},
            {"gate_id": "CG3090_2_vertical_quotient_closed", "claim": "X is absent/vertical before variation", "gate_pass": False, "reason": "q map, vertical generator, action/matter descent and boundary silence are not yet built together", "claim_allowed_for_physics": False},
            {"gate_id": "CG3090_3_scalar_nohair", "claim": "scalar no-hair gives local silence", "gate_pass": False, "reason": "scalar branch requires real Z_X, M_X2, J_X and parent-selected boundary data", "claim_allowed_for_physics": False},
            {"gate_id": "CG3090_4_edge_bound_executable", "claim": "first edge-bound row is executable", "gate_pass": False, "reason": "EDGEBOUND terms have missing source paths and units", "claim_allowed_for_physics": False},
            {"gate_id": "CG3090_5_local_GR_Newton", "claim": "local GR/Newton reduction passes", "gate_pass": False, "reason": "local source branch remains theorem-unclosed and unbounded", "claim_allowed_for_physics": False},
            {"gate_id": "CG3090_6_route_guardrail", "claim": "route separation guardrail is installed", "gate_pass": True, "reason": "vertical quotient, scalar no-hair and edge-bound residual routes are separated", "claim_allowed_for_physics": False},
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "decision_id": "DEC3090_0_primitive_result",
                "decision": "BX_PRIMITIVE_NOT_DERIVED",
                "reason": "parent L_X/Theta_X/Q_X/P_X/B_ct chain is an audit contract, not a signed parent variation",
                "next_action": "do not claim Q_edge zero; attack branch-choice theorem directly",
            },
            {
                "decision_id": "DEC3090_1_route_split",
                "decision": "KEEP_GAUGE_EDGE_SCALAR_AND_BOUND_ROUTES_SEPARATE",
                "reason": "scalar positivity can silence an X field under source-free conditions but does not automatically supply a Noether edge primitive",
                "next_action": "test quotient/vertical construction first, scalar no-hair second, edge-bound third",
            },
            {
                "decision_id": "DEC3090_2_best_next",
                "decision": "VERTICAL_QUOTIENT_CONSTRUCTION_IS_LEAST_SCRUTINY_ROUTE",
                "reason": "removing X before variation is cleaner than bounding a leftover local coupling after the fact",
                "next_action": "3091-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice-under-AX1090.md",
            },
            {
                "decision_id": "DEC3090_3_fallback",
                "decision": "IF_QUOTIENT_FAILS_FILL_EDGEBOUND_AND_SCALAR_COEFFICIENTS",
                "reason": "then MTS survives or fails as a bounded residual theory rather than a theorem-zero local-GR branch",
                "next_action": "fill EBF3090 terms plus Z_X/M_X2/J_X/K_X/Qbar/qbar rows as nonclaim",
            },
        ]
    )


def next_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "next_id": "NEXT3090_0_3091",
                "next_checkpoint": "3091-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice-under-AX1090.md",
                "script": "scripts/Y5_R2FR_vertical_quotient_LX_construction_or_scalar_nohair_branch_choice_under_AX1090_3091.py",
                "mission": "choose/test the least-scrutiny local branch: construct X as absent/vertical quotient before variation, or demote to scalar positive no-hair/source-coefficient route",
                "starting_equation": "q(Phi+epsilon v_X)=q(Phi), Dq[v_X]=0, S_parent=Sbar[q(Phi)] and Q_edge[v_X]=0; otherwise O_X X=J_X with EDGEBOUND fallback",
                "claim_policy": "no Q_edge zero, scalar local silence, R10/R11, PPN, clock, orbital, Newton or local-GR claim unless quotient descent closes or scalar/source rows are source-backed nonclaim",
            }
        ]
    )


def branch_copy_rows() -> list[dict[str, Any]]:
    mapping = {
        "BR3090_0_primitive": (OUTPUTS["primitive_gates"], BRANCH_OUTPUTS["primitive_copy"]),
        "BR3090_1_branch_split": (OUTPUTS["branch_split"], BRANCH_OUTPUTS["branch_split_copy"]),
        "BR3090_2_edge_fill": (OUTPUTS["edge_fill"], BRANCH_OUTPUTS["edge_fill_copy"]),
        "BR3090_3_bridge": (OUTPUTS["bridge"], BRANCH_OUTPUTS["bridge_copy"]),
        "BR3090_4_next": (OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
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


def markdown_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for output_row in output_rows:
        lines.append("| " + " | ".join(str(output_row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    parent_variation: list[dict[str, Any]],
    primitive_gates: list[dict[str, Any]],
    branch_split: list[dict[str, Any]],
    edge_fill: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    body = f"""# 3090 - B_X Primitive From Parent Variation or Edge-Bound Term

Status: `Y5_R2FR_3090_BX_primitive_not_derived_branch_split_installed`

## Verdict

`B_X` is still not derivable from the current files. The parent variation chain is explicit, but `L_X/Theta_X/Q_X/P_X/B_ct` remain contracts rather than a signed parent action. That means no `B_X=d_S b_X`, no `Q_edge=0`, and no local Newton/GR claim follows from this checkpoint.

The useful progress is a clean branch split: first try the vertical quotient route, second try scalar positive no-hair as a separate theorem, and third fill weighted-Stokes edge-bound terms as nonclaim source rows. No more mixing a scalar boundary condition with a Noether edge-zero proof.

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "parse_ok", "needles_present", "missing_needles", "role"])}

## Parent Variation Template

{markdown_table(parent_variation, ["template_id", "object", "formula", "closure_test", "current_status", "implication"])}

## B_X Primitive Gates

{markdown_table(primitive_gates, ["gate_id", "primitive_requirement", "test", "current_result", "missing_for_claim", "if_missing"])}

## Branch Separation

{markdown_table(branch_split, ["branch_id", "branch", "formula", "status", "why", "next_test"])}

## Edge-Bound Fill Schema

{markdown_table(edge_fill, ["fill_id", "quantity", "definition", "required_source", "current_status", "units", "source_path"])}

## Route Verdicts

{markdown_table(routes, ["route_id", "route", "status", "because", "next_step"])}

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
    sources = rows(OUTPUTS["sources"])
    parent_variation = rows(OUTPUTS["parent_variation"])
    primitive_gates = rows(OUTPUTS["primitive_gates"])
    branch_split = rows(OUTPUTS["branch_split"])
    edge_fill = rows(OUTPUTS["edge_fill"])
    routes = rows(OUTPUTS["route_verdicts"])
    bridge = rows(OUTPUTS["bridge"])
    gates = rows(OUTPUTS["gates"])
    decisions = rows(OUTPUTS["decisions"])
    next_target = rows(OUTPUTS["next"])

    checks: list[tuple[str, bool, str, str]] = [
        ("VAL3090_00_sources_exist", all(boolish(row["exists"]) for row in sources), "all cited source paths exist", "P8_Y5_R2FR_3090_SOURCE_REGISTER.csv"),
        ("VAL3090_01_needles_present", all(boolish(row["needles_present"]) for row in sources), "all cited source needles are present", "P8_Y5_R2FR_3090_SOURCE_REGISTER.csv"),
        ("VAL3090_02_sources_parse", all(boolish(row["parse_ok"]) for row in sources), "all cited CSV sources parse and markdown sources exist", "P8_Y5_R2FR_3090_SOURCE_REGISTER.csv"),
        ("VAL3090_03_csv_parse", all(csv_ok(path) for path in generated_paths + branch_paths), "all generated and branch-copy CSVs parse cleanly", "csv.DictReader parse check"),
        ("VAL3090_04_parent_map_complete", len(parent_variation) >= 6 and any(row["template_id"] == "PVT3090_5_verdict" for row in parent_variation), "parent variation to primitive map is complete", "P8_Y5_R2FR_3090_PARENT_VARIATION_TEMPLATE.csv"),
        ("VAL3090_05_parent_map_blocks_claim", any(row["current_status"] == "MAP_WRITTEN_NOT_CLOSED" for row in parent_variation), "parent variation map remains nonclaim", "P8_Y5_R2FR_3090_PARENT_VARIATION_TEMPLATE.csv"),
        ("VAL3090_06_primitive_gates_complete", len(primitive_gates) >= 6 and any(row["gate_id"] == "BXG3090_5_verdict" for row in primitive_gates), "primitive gates cover same-parent, counterterm, exact pullback, harmonic, kernel and verdict", "P8_Y5_R2FR_3090_BX_PRIMITIVE_GATES.csv"),
        ("VAL3090_07_primitive_blocks_claim", any(row["current_result"] == "FAIL_CURRENT_CLAIM" for row in primitive_gates), "B_X primitive remains blocked", "P8_Y5_R2FR_3090_BX_PRIMITIVE_GATES.csv"),
        ("VAL3090_08_branch_split_complete", {"BRS3090_0_vertical_quotient", "BRS3090_2_scalar_nohair", "BRS3090_3_edge_bound", "BRS3090_4_route_guardrail"}.issubset({row["branch_id"] for row in branch_split}), "vertical, scalar and edge-bound routes are separated", "P8_Y5_R2FR_3090_BRANCH_SEPARATION.csv"),
        ("VAL3090_09_branch_split_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in branch_split), "branch split rows remain nonclaim", "P8_Y5_R2FR_3090_BRANCH_SEPARATION.csv"),
        ("VAL3090_10_edge_fill_complete", len(edge_fill) >= 6 and any(row["fill_id"] == "EBF3090_5_verdict" for row in edge_fill), "edge-bound fill schema covers primitive, harmonic, residual, kernel, corner and verdict", "P8_Y5_R2FR_3090_EDGE_BOUND_FILL_SCHEMA.csv"),
        ("VAL3090_11_edge_fill_not_executable", any(row["current_status"] == "NOT_FILLABLE_CURRENTLY" for row in edge_fill), "edge-bound first row remains not fillable", "P8_Y5_R2FR_3090_EDGE_BOUND_FILL_SCHEMA.csv"),
        ("VAL3090_12_missing_rows_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in edge_fill + primitive_gates), "MISSING rows stay nonclaim", "P8_Y5_R2FR_3090_EDGE_BOUND_FILL_SCHEMA.csv;BX_PRIMITIVE_GATES.csv"),
        ("VAL3090_13_route_verdict_nonclaim", any(row["route_id"] == "R3090_4_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_BUT_SPLITS_ROUTES" for row in routes), "route verdict splits theorem routes without claim promotion", "P8_Y5_R2FR_3090_ROUTE_VERDICTS.csv"),
        ("VAL3090_14_bridge_next_selected", any(row["status_id"] == "GB3090_5_next" and "VERTICAL_QUOTIENT" in row["current_status"] for row in bridge), "bridge status selects vertical quotient/scalar branch choice next", "P8_Y5_R2FR_3090_GR_BRIDGE_STATUS.csv"),
        ("VAL3090_15_bridge_nonclaim", all(str(row["bridge_claim"]).lower() == "false" for row in bridge), "GR bridge rows remain nonclaim", "P8_Y5_R2FR_3090_GR_BRIDGE_STATUS.csv"),
        ("VAL3090_16_claim_gates_blocked", all(str(row["claim_allowed_for_physics"]).lower() == "false" for row in gates), "all claim gates are nonclaim", "P8_Y5_R2FR_3090_CLAIM_GATE.csv"),
        ("VAL3090_17_local_GR_gate_false", any(row["gate_id"] == "CG3090_5_local_GR_Newton" and str(row["gate_pass"]).lower() == "false" for row in gates), "local GR/Newton gate remains false", "P8_Y5_R2FR_3090_CLAIM_GATE.csv"),
        ("VAL3090_18_guardrail_pass_only_nonclaim", any(row["gate_id"] == "CG3090_6_route_guardrail" and str(row["gate_pass"]).lower() == "true" and str(row["claim_allowed_for_physics"]).lower() == "false" for row in gates), "route guardrail passes but opens no physics claim", "P8_Y5_R2FR_3090_CLAIM_GATE.csv"),
        ("VAL3090_19_decision_best_next", any(row["decision"] == "VERTICAL_QUOTIENT_CONSTRUCTION_IS_LEAST_SCRUTINY_ROUTE" for row in decisions), "decision ledger selects least-scrutiny vertical quotient route first", "P8_Y5_R2FR_3090_DECISION_LEDGER.csv"),
        ("VAL3090_20_next_target_selected", len(next_target) == 1 and next_target[0]["next_id"] == "NEXT3090_0_3091", "next target selected", "P8_Y5_R2FR_3090_NEXT_TARGET.csv"),
        ("VAL3090_21_branch_copies_exist", all(path.exists() for path in branch_paths), "branch copy CSVs exist", "P8_Y5_R2FR_3090_BRANCH_COPIES.csv"),
        ("VAL3090_22_formalization_untouched", not any(FORMALIZATION.rglob("*3090*")) if FORMALIZATION.exists() else True, "no 3090 files exist under formalization-workbench", str(FORMALIZATION)),
        ("VAL3090_23_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ removed", str(PYCACHE)),
        ("VAL3090_24_doc_written", DOC.exists() and "BX_primitive_not_derived_branch_split_installed" in file_text(DOC), "checkpoint markdown is written with nonclaim verdict", str(DOC)),
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

    sources = source_register_rows()
    parent_variation = parent_variation_rows()
    primitive_gates = primitive_gate_rows()
    branch_split = branch_split_rows()
    edge_fill = edge_fill_rows()
    routes = route_verdict_rows()
    bridge = bridge_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["parent_variation"], parent_variation)
    write_csv(OUTPUTS["primitive_gates"], primitive_gates)
    write_csv(OUTPUTS["branch_split"], branch_split)
    write_csv(OUTPUTS["edge_fill"], edge_fill)
    write_csv(OUTPUTS["route_verdicts"], routes)
    write_csv(OUTPUTS["bridge"], bridge)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    copy_map = {
        OUTPUTS["primitive_gates"]: BRANCH_OUTPUTS["primitive_copy"],
        OUTPUTS["branch_split"]: BRANCH_OUTPUTS["branch_split_copy"],
        OUTPUTS["edge_fill"]: BRANCH_OUTPUTS["edge_fill_copy"],
        OUTPUTS["bridge"]: BRANCH_OUTPUTS["bridge_copy"],
        OUTPUTS["next"]: BRANCH_OUTPUTS["next_copy"],
    }
    for source, destination in copy_map.items():
        shutil.copyfile(source, destination)
    branch_copies = branch_copy_rows()
    write_csv(OUTPUTS["branches"], branch_copies)

    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    validation = validate(generated_paths, branch_paths)
    write_doc(sources, parent_variation, primitive_gates, branch_split, edge_fill, routes, bridge, gates, decisions, next_target, validation)
    validation = validate(generated_paths, branch_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, parent_variation, primitive_gates, branch_split, edge_fill, routes, bridge, gates, decisions, next_target, validation)

    remove_pycache()
    validation = validate(generated_paths, branch_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, parent_variation, primitive_gates, branch_split, edge_fill, routes, bridge, gates, decisions, next_target, validation)

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
