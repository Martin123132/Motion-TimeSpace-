from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1828"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
P4_RUN = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1828-Y5-R2FR-connection-hinge-bivector-owner-or-c2-map-fill.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1828_0_1827_next",
        "source_key": "1827_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_NEXT_TARGET.csv",
        "needles": ["NEXT1827_0_primary", "selected"],
        "role": "1827 selects connection/hinge owner or finite c2 map fill.",
    },
    {
        "source_id": "SRC1828_1_1827_validation",
        "source_key": "1827_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1827_VALIDATION.csv",
        "needles": ["VAL1827_OVERALL", "PASS"],
        "role": "confirms 1827 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1828_2_1827_field_match",
        "source_key": "1827_field_match",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_PALATINI_FIELD_MATCH_ATTEMPT.csv",
        "needles": ["FMA1827_2_connection", "MISSING_CONNECTION_COMPATIBILITY"],
        "role": "connection compatibility is the main Palatini field-match blocker.",
    },
    {
        "source_id": "SRC1828_3_1827_block_map",
        "source_key": "1827_block_map",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_PALATINI_BLOCK_MAP.csv",
        "needles": ["PBM1827_3_Bh_Ah", "MISSING_HINGE_OWNER"],
        "role": "oriented hinge bivector/area owner is missing.",
    },
    {
        "source_id": "SRC1828_4_P4_problem",
        "source_key": "P4_problem_statement",
        "source_path": P4_RUN / "P4_problem_statement.csv",
        "needles": ["P4_target", "central_blocker_not_parent_derived"],
        "role": "P4 connection problem states the Levi-Civita/connection target and blocker.",
    },
    {
        "source_id": "SRC1828_5_P4_routes",
        "source_key": "P4_compatibility_routes",
        "source_path": P4_RUN / "compatibility_theorem_routes.csv",
        "needles": ["P4_R0_metric_formalism_if_parent_selects_only_g", "conditional_not_parent_derived"],
        "role": "metric-only, Palatini, torsion, metric-affine, and projective connection routes are conditional only.",
    },
    {
        "source_id": "SRC1828_6_P4_gate",
        "source_key": "P4_gate_results",
        "source_path": P4_RUN / "gate_results.csv",
        "needles": ["torsion_zero_derived", "nonmetricity_zero_derived"],
        "role": "prior P4 gate records torsion and nonmetricity zeros as failed.",
    },
    {
        "source_id": "SRC1828_7_1045_connection_stack",
        "source_key": "1045_connection_stack",
        "source_path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "needles": ["QG1045_2_connection_stack", "CONDITIONAL_CONNECTION_CAVEAT"],
        "role": "matter-functor descent retains the connection caveat.",
    },
    {
        "source_id": "SRC1828_8_1010_Gamma_Khat",
        "source_key": "1010_Gamma_Khat_action",
        "source_path": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "needles": ["GKT1010_1_metric_response_identity", "not_matched_to_current_symbols"],
        "role": "Gamma_eff/K_hat metric-response identity remains unmatched.",
    },
    {
        "source_id": "SRC1828_9_1823_Regge",
        "source_key": "1823_Regge_bridge",
        "source_path": ROOT / "1823-Y5-R2FR-primitive-deficit-action-law-or-visible-c2-owner-row.md",
        "needles": ["DAL1823_1_Regge_EH_bridge", "MTS_PRIMITIVE_ACTION_LAW_UNSIGNED"],
        "role": "Regge/EH area-deficit bridge is conditional but MTS primitive action law remains unsigned.",
    },
    {
        "source_id": "SRC1828_10_1827_c2_map",
        "source_key": "1827_c2_scalaron_map",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_C2_SCALARON_MAP_CONTRACT.csv",
        "needles": ["CSM1827_4_total", "C2_SCALARON_MAP_CONTRACT_READY_NONCLAIM"],
        "role": "finite c2 scalaron fallback contract is ready but nonclaim.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_SOURCE_REGISTER.csv",
    "connection_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_CONNECTION_COMPATIBILITY_AUDIT.csv",
    "hinge_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_HINGE_BIVECTOR_OWNER_AUDIT.csv",
    "c2_map_fill": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_C2_MAP_FIRST_FILL_LEDGER.csv",
    "geometry_decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_GEOMETRY_DECISION_MATRIX.csv",
    "local_gr_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_LOCAL_GR_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1828_VALIDATION.csv",
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


def connection_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CCA1828_0_target",
            "route": "Gamma_eff/omega_obs compatibility",
            "test": "prove the observed connection is omega[e_obs] or an independent Palatini/metric-affine connection whose torsion, nonmetricity, projective residue and matter hypermomentum are silent",
            "current_status": "TARGET_ATTEMPTED",
            "blocker": "prior P4 gates show the required zero theorems are not parent-derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CCA1828_1_metric_only",
            "route": "metric/coframe-only parent configuration",
            "test": "parent selects only g_obs/e_obs, so Gamma is definitionally Levi-Civita/spin connection",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "blocker": "current corpus uses omega[e] in places but does not derive absence of independent connection variables",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CCA1828_2_Palatini",
            "route": "Palatini EH variation",
            "test": "EH Palatini action plus matter independent of Gamma forces Levi-Civita up to harmless projective freedom",
            "current_status": "BLOCKED_BY_OPEN_EH_AND_MATTER_PREMISES",
            "blocker": "EH-only is not derived and matter/light/spin independence from Gamma is not proven",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CCA1828_3_torsion",
            "route": "first-order coframe zero-torsion route",
            "test": "spin-connection variation imposes vanishing torsion",
            "current_status": "NOT_PARENT_DERIVED",
            "blocker": "ordinary spinor matter can source Einstein-Cartan torsion unless explicitly excluded or mapped",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CCA1828_4_metric_affine",
            "route": "metric-affine zero-Q zero-T theorem",
            "test": "algebraic connection equations force torsion and nonmetricity to zero with no source term",
            "current_status": "NOT_SUPPLIED",
            "blocker": "no current action-level equation supplies zero-source algebraic connection theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CCA1828_5_Gamma_eff",
            "route": "current Gamma_eff/K_hat symbols",
            "test": "identify Gamma_eff with omega[e_obs] or with a metric-response action whose K_hat closes the Ward residual",
            "current_status": "NOT_MATCHED_TO_CURRENT_SYMBOLS",
            "blocker": "K_hat metric response and Helmholtz/action-existence checks remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CCA1828_6_verdict",
            "route": "connection compatibility closes",
            "test": "CCA1828_1 through CCA1828_5 close in one parent geometry",
            "current_status": "CONNECTION_OWNER_FAILS_CURRENT_CORPUS",
            "blocker": "Levi-Civita compatibility remains a theorem-or-P4-vector fork",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def hinge_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HBA1828_0_target",
            "route": "oriented hinge bivector / area owner",
            "test": "construct B_h = integral_h e wedge e, A_h, and signed orientation from MTS local cell/domain geometry",
            "current_status": "TARGET_ATTEMPTED",
            "blocker": "MTS cell/domain grammar does not yet define Regge hinges",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HBA1828_1_coframe_area",
            "route": "coframe area form",
            "test": "if e_obs is owned, e wedge e supplies a geometric area bivector",
            "current_status": "MATH_OK_PARENT_PREMISE_UNSIGNED",
            "blocker": "e_obs/coframe descent remains conditional",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HBA1828_2_cell_complex",
            "route": "MTS cell-to-hinge complex",
            "test": "parent domain/cell geometry selects local hinges/faces carrying curvature deficits",
            "current_status": "MISSING_CELL_COMPLEX_OWNER",
            "blocker": "no triangulation/hinge selection, adjacency rule, or refinement law is parent-derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HBA1828_3_orientation",
            "route": "physical hinge orientation",
            "test": "relative-chain/boundary orientation fixes the sign of A_h delta_h as physical rather than gauge relabeling",
            "current_status": "ORIENTATION_STILL_UNSIGNED",
            "blocker": "orientation route exists only as partial nonclaim support",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HBA1828_4_scale_shape",
            "route": "cell scale and shape factor",
            "test": "ell_cell, shape factor and continuum refinement map are fixed by parent geometry",
            "current_status": "MISSING_SCALE_SHAPE_REFINEMENT",
            "blocker": "without these, c_R2_eff and Regge continuum normalization remain unscored",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HBA1828_5_verdict",
            "route": "hinge bivector owner closes",
            "test": "HBA1828_1 through HBA1828_4 close in one MTS cell geometry",
            "current_status": "HINGE_OWNER_FAILS_CURRENT_CORPUS",
            "blocker": "area form is mathematically available only after coframe/cell/orientation/scale ownership is derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def c2_map_fill_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "fill_id": "C2F1828_0_c2",
            "quantity": "c2_visible",
            "first_fill": "carry from 1827: c2_visible = 1/2 Phi''(0)",
            "missing_inputs": "parent Phi; finite value or zero theorem; uncertainty; source path",
            "current_status": "MISSING_PARENT_PHI_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "C2F1828_1_cell",
            "quantity": "ell_cell and shape_factor",
            "first_fill": "needed for c_R2_eff ~ shape_factor * c2_visible * ell_cell^2 / EH_normalization",
            "missing_inputs": "cell complex; hinge area; refinement law; continuum normalization",
            "current_status": "MISSING_HINGE_CELL_SCALE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "C2F1828_2_connection_interlock",
            "quantity": "P4 connection residual",
            "first_fill": "finite c2/R2 map cannot claim local-GR safety while torsion/nonmetricity rows remain template-only",
            "missing_inputs": "derived Levi-Civita theorem or executable P4 connection coefficients and maps",
            "current_status": "P4_CONNECTION_INTERLOCK_OPEN",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "C2F1828_3_observables",
            "quantity": "R10/PPN/clock/orbital projections",
            "first_fill": "map c_R2_eff/scalar mode into alpha(lambda), gamma, beta, clocks and source normalization",
            "missing_inputs": "linearized scalar mode; matter coupling; source charge; official bounds; units",
            "current_status": "MISSING_OBSERVABLE_PROJECTION",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "C2F1828_4_total",
            "quantity": "finite c2 map first-fill status",
            "first_fill": "schema is now attached to connection and hinge debts",
            "missing_inputs": "C2F1828_0 through C2F1828_3 all sourced",
            "current_status": "FIRST_FILL_LEDGER_READY_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def geometry_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "GDM1828_0_connection",
            "route": "derive connection compatibility",
            "current_result": "FAIL_CURRENT_CORPUS",
            "reason": "metric-only, Palatini, torsion, metric-affine and Gamma_eff routes are all conditional or unsigned",
            "next_action": "try metric-only parent configuration theorem or fill P4 connection rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "GDM1828_1_hinge",
            "route": "derive oriented hinge bivector",
            "current_result": "FAIL_CURRENT_CORPUS",
            "reason": "coframe area math is fine, but cell complex, orientation and scale/refinement are not parent-owned",
            "next_action": "derive cell-complex/hinge owner or carry ell_cell/shape_factor as sourced residual inputs",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "GDM1828_2_c2",
            "route": "finite c2 map fill",
            "current_result": "NONCLAIM_LEDGER_READY",
            "reason": "fallback is now tied to c2, cell scale, P4 connection and observable projection debts",
            "next_action": "do not score until numeric/source-backed inputs exist",
            "valid_for_claim": False,
        },
    ]


def local_gr_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1828_0_if_connection_hinge_close",
            "if_closed": "connection compatibility and hinge bivector owner are parent-signed",
            "would_buy": "Palatini/Regge linear action route becomes much less speculative",
            "still_missing": "matter/Pi_M source descent, variation, higher operators, q_loc and PPN maps",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1828_1_if_fail",
            "if_closed": "connection or hinge owner remains unsigned",
            "would_buy": "clean demotion to P4 connection rows plus c2 scalaron residual branch",
            "still_missing": "real coefficients, units, bounds, and no-cancellation policy",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1828_2_verdict",
            "if_closed": "1828 alone proves local GR/Newton",
            "would_buy": "nothing claimable alone",
            "still_missing": "connection and hinge owners both fail current corpus",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1828_0_geometry_audit",
            "gate": "connection and hinge audits written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "1828 isolates the geometry-owner blockers",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1828_1_connection_owner",
            "gate": "connection owner parent-signed",
            "current_status": "BLOCKED",
            "reason": "P4 theorem-or-vector fork remains open",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1828_2_hinge_owner",
            "gate": "hinge bivector/area owner parent-signed",
            "current_status": "BLOCKED",
            "reason": "cell complex, orientation and scale are missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1828_3_c2_map",
            "gate": "finite c2 map score-ready",
            "current_status": "BLOCKED",
            "reason": "first-fill ledger contains missing parent inputs",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1828_0_connection",
            "claim": "Gamma_eff/omega_obs compatibility derived",
            "status": "BLOCKED",
            "reason": "torsion/nonmetricity/independent connection routes are not parent-signed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1828_1_hinge",
            "claim": "oriented hinge bivector/area derived",
            "status": "BLOCKED",
            "reason": "cell complex and orientation ownership are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1828_2_c2_score",
            "claim": "finite c2 map can be scored",
            "status": "BLOCKED",
            "reason": "c2, cell scale, connection residual and observable maps are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1828_3_local_GR",
            "claim": "local GR/Newton reduction follows",
            "status": "REFUSED",
            "reason": "geometry-owner checkpoint only; no source/PPN/local-GR promotion",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1828_0_connection_result",
            "decision": "CONNECTION_OWNER_NOT_DERIVED",
            "reason": "prior P4 compatibility routes remain conditional and current Gamma_eff is not matched to omega[e_obs]",
            "next_action": "do not use Palatini/Regge route as a claim yet",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1828_1_hinge_result",
            "decision": "HINGE_BIVECTOR_OWNER_NOT_DERIVED",
            "reason": "coframe area is only conditional; no MTS cell-complex/hinge orientation/refinement law exists yet",
            "next_action": "derive cell complex and orientation, or source ell_cell/shape_factor",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1828_2_best_next",
            "decision": "METRIC_ONLY_CONNECTION_THEOREM_OR_P4_HINGE_SOURCE_PACK_NEXT",
            "reason": "the least-cheaty route is to prove the parent has only the observed coframe/metric connection; fallback is P4 rows plus hinge/c2 source pack",
            "next_action": "1829-Y5-R2FR-metric-only-connection-theorem-or-P4-hinge-source-pack.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1828_0_primary",
            "next_target": "1829-Y5-R2FR-metric-only-connection-theorem-or-P4-hinge-source-pack.md",
            "script": "scripts/Y5_R2FR_metric_only_connection_theorem_or_P4_hinge_source_pack.py",
            "objective": "derive that the parent configuration has only the observed metric/coframe connection; if not, fill P4 connection rows plus hinge cell-scale/c2 source-pack rows as nonclaim",
            "selection_status": "selected",
            "success_condition": "metric-only connection theorem parent-signed, or P4/hinge/c2 rows remain valid_for_claim=false with all missing inputs explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1828_1_parallel",
            "next_target": "1829b-Y5-R2FR-cell-complex-orientation-refinement-law.md",
            "script": "scripts/Y5_R2FR_cell_complex_orientation_refinement_law.py",
            "objective": "derive Regge-style cell/hinge complex, orientation and refinement/shape factor if the connection theorem closes",
            "selection_status": "held_parallel",
            "success_condition": "B_h/A_h, ell_cell and shape_factor become parent-derived or retained as explicit source inputs",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "connection_audit": connection_audit_rows(),
        "hinge_audit": hinge_audit_rows(),
        "c2_map_fill": c2_map_fill_rows(),
        "geometry_decision": geometry_decision_rows(),
        "local_gr_impact": local_gr_impact_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "claim_gate": claim_gate_rows(),
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
    guarded_keys = {"valid_for_claim", "claim_allowed", "score_ready"}
    for rows in rows_map.values():
        for row in rows:
            for key in guarded_keys.intersection(row):
                if str(row[key]).lower() == "true":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness_keys = ["valid_for_claim", "claim_allowed", "score_ready"]
    for rows in rows_map.values():
        for row in rows:
            has_missing = any("MISSING" in str(value) for value in row.values())
            if not has_missing:
                continue
            if any(str(row.get(key, "")).lower() == "true" for key in readiness_keys):
                return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if "1828-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1828") or name.startswith("P8_Y5_BRR545_1828"):
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
    checks: list[tuple[str, bool, str]] = [
        ("VAL1828_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1828_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        ("VAL1828_2_connection_audit_written", any(row["audit_id"] == "CCA1828_0_target" for row in rows_map["connection_audit"]), "connection audit is written"),
        (
            "VAL1828_3_connection_not_promoted",
            any(row["audit_id"] == "CCA1828_6_verdict" and row["current_status"] == "CONNECTION_OWNER_FAILS_CURRENT_CORPUS" for row in rows_map["connection_audit"]),
            "connection owner fails current corpus",
        ),
        ("VAL1828_4_hinge_audit_written", any(row["audit_id"] == "HBA1828_0_target" for row in rows_map["hinge_audit"]), "hinge audit is written"),
        (
            "VAL1828_5_hinge_not_promoted",
            any(row["audit_id"] == "HBA1828_5_verdict" and row["current_status"] == "HINGE_OWNER_FAILS_CURRENT_CORPUS" for row in rows_map["hinge_audit"]),
            "hinge owner fails current corpus",
        ),
        (
            "VAL1828_6_c2_fill_nonclaim",
            any(row["fill_id"] == "C2F1828_4_total" and row["current_status"] == "FIRST_FILL_LEDGER_READY_NONCLAIM" and row["score_ready"] is False for row in rows_map["c2_map_fill"]),
            "c2 first-fill ledger is nonclaim",
        ),
        (
            "VAL1828_7_decision_matrix_nonclaim",
            all(row["valid_for_claim"] is False for row in rows_map["geometry_decision"]),
            "geometry decision rows are nonclaim",
        ),
        (
            "VAL1828_8_local_gr_nonclaim",
            all(row["claim_allowed_now"] is False and row["valid_for_claim"] is False for row in rows_map["local_gr_impact"]),
            "local GR impact rows remain nonclaim",
        ),
        (
            "VAL1828_9_acceptance_blocks",
            any(row["gate_id"] == "AC1828_0_geometry_audit" and row["gate_pass"] is True and row["claim_allowed"] is False for row in rows_map["acceptance_gate"])
            and all(row["claim_allowed"] is False for row in rows_map["acceptance_gate"]),
            "acceptance gate allows contract-only progress and blocks claims",
        ),
        (
            "VAL1828_10_claim_gates_blocked",
            all(row["gate_pass"] is False and row["valid_for_claim"] is False for row in rows_map["claim_gate"]),
            "all connection/hinge/c2/local-GR claim gates remain blocked or refused",
        ),
        ("VAL1828_11_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1828_12_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1828_13_decision_next",
            any(row["decision_id"] == "DEC1828_2_best_next" and row["decision"] == "METRIC_ONLY_CONNECTION_THEOREM_OR_P4_HINGE_SOURCE_PACK_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects metric-only connection theorem or P4/hinge source pack next",
        ),
        (
            "VAL1828_14_next_selected",
            any(row["route_id"] == "NEXT1828_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1828_15_csv_parse", csv_parse_ok(output_paths), "all generated 1828 CSVs parse"),
        ("VAL1828_16_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1828_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1828_18_formalization_untouched", no_formalization_outputs(), "no 1828 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1828_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1828 connection-hinge bivector owner or c2 map fill checkpoint",
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
            "# 1828 Y5 R2FR connection hinge bivector owner or c2 map fill",
            "",
            "**Progress:** 1828 attacks the geometry fork directly. The connection side does not close: metric-only, Palatini, torsion, metric-affine, projective, and current `Gamma_eff/K_hat` routes are all conditional or unsigned. The hinge side also does not close: `e wedge e` is mathematically available only after the coframe, cell complex, orientation, and refinement scale are parent-owned.",
            "",
            "**Current verdict:** no Palatini/Regge promotion. The least-cheaty next derivation is a metric-only connection theorem: prove the parent configuration has only the observed metric/coframe connection. If that fails, the honest fallback is explicit P4 connection rows plus hinge cell-scale and finite `c2` source-pack rows.",
            "",
            "**Claim ceiling:** no connection compatibility claim, no hinge-bivector claim, no `c2` score, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1828.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Connection Compatibility Audit",
            markdown_table(rows_map["connection_audit"], ["audit_id", "route", "test", "current_status", "blocker", "claim_allowed", "valid_for_claim"]),
            "",
            "## Hinge Bivector Owner Audit",
            markdown_table(rows_map["hinge_audit"], ["audit_id", "route", "test", "current_status", "blocker", "claim_allowed", "valid_for_claim"]),
            "",
            "## C2 Map First Fill Ledger",
            markdown_table(rows_map["c2_map_fill"], ["fill_id", "quantity", "first_fill", "missing_inputs", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Geometry Decision Matrix",
            markdown_table(rows_map["geometry_decision"], ["decision_id", "route", "current_result", "reason", "next_action", "valid_for_claim"]),
            "",
            "## Local GR Impact",
            markdown_table(rows_map["local_gr_impact"], ["impact_id", "if_closed", "would_buy", "still_missing", "claim_allowed_now", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "claim_allowed", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
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
            "This checkpoint says the Palatini/Regge route is still alive but not free. The cleanest possible win is now very specific: MTS must prove it has no independent local connection beyond the observed coframe/metric connection. If that proof fails, the project should stop trying to smuggle in Levi-Civita geometry and instead carry torsion/nonmetricity/P4 plus finite `c2` rows into the empirical bound machinery.",
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
    print(f"1828 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
