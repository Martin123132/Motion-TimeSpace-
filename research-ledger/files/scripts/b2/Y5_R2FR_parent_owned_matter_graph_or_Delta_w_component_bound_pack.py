from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1606"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1606-Y5-R2FR-parent-owned-matter-graph-or-Delta_w-component-bound-pack.md"

SOURCE_FILES = {
    "1605_doc": ROOT / "1605-Y5-R2FR-action-density-owner-or-finite-C_EP-evidence-import.md",
    "1605_validation": OUT / "P8_Y5_BRR545_1605_VALIDATION.csv",
    "1605_action_owner": OUT / "P8_Y5_PARENT_QLOC_1605_ACTION_DENSITY_OWNER_THEOREM_ATTEMPT.csv",
    "1605_graph": OUT / "P8_Y5_PARENT_QLOC_1605_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv",
    "1605_reduction": OUT / "P8_Y5_PARENT_QLOC_1605_NO_WA_REDUCTION_STATUS.csv",
    "1605_next": OUT / "P8_Y5_PARENT_QLOC_1605_NEXT_TARGET.csv",
    "1477_graph": COEFF / "connected_matter_graph_certificate_nonclaim_1477.csv",
    "1464_connected": COEFF / "connected_matter_category_proof_attempt_1464.csv",
    "1477_source_gates": COEFF / "source_weight_reduction_gates_1477.csv",
    "1476_delta_input": COEFF / "Ci_source_weight_delta_w_input_nonclaim_1476.csv",
    "1477_delta_schema": COEFF / "delta_w_tau_wep_schema_v2_nonclaim_1477.csv",
    "1478_component_vector": COEFF / "component_delta_w_vector_template_nonclaim_1478.csv",
    "1479_component_pack": COEFF / "component_delta_w_bound_pack_nonclaim_1479.csv",
    "1481_material_context": COEFF / "WEP_material_context_pack_nonclaim_1481.csv",
}

NEEDLES = {
    "1605_doc": ["ADO1605_6_verdict", "ACTION_DENSITY_OWNER_NOT_PARENT_SIGNED"],
    "1605_validation": ["VAL1605_OVERALL", "PASS"],
    "1605_action_owner": ["ADO1605_1_naturality_lemma", "EXACT_CONDITIONAL_LEMMA"],
    "1605_graph": ["GRC1605_6_verdict", "physical connectedness is not enough"],
    "1605_reduction": ["RED1605_6_verdict", "Delta_w_A theorem-zero"],
    "1605_next": ["1606-Y5-R2FR-parent-owned-matter-graph-or-Delta_w-component-bound-pack.md", "Delta_w component bound rows"],
    "1477_graph": ["GRC1477_1_parent_owned_connectivity", "FAIL_NOT_PARENT_SIGNED"],
    "1464_connected": ["CON1464_5_verdict", "PROOF_NOT_CLOSED"],
    "1477_source_gates": ["GATE1477_1_parent_owned_graph", "False"],
    "1476_delta_input": ["DW1476_0_delta_w_A", "parent theorem-zero certificate OR numeric/source-backed"],
    "1477_delta_schema": ["SC1477_16", "valid_for_claim"],
    "1478_component_vector": ["CDW1478_0_parent_component_vector", "delta_w_component_vector"],
    "1479_component_pack": ["CBP1479_1_delta_w_e", "PROXY_UNIT_KERNEL_ONLY"],
    "1481_material_context": ["MAT1481_6_full_tensor", "BLOCKED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1606_SOURCE_REGISTER.csv"
GRAPH_OWNER = OUT / "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_GRAPH_THEOREM_ATTEMPT.csv"
EDGE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv"
COMPONENT_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1606_DELTA_W_COMPONENT_BOUND_SCHEMA.csv"
COMPONENT_PACK = OUT / "P8_Y5_PARENT_QLOC_1606_DELTA_W_COMPONENT_BOUND_PACK.csv"
SCORE_READINESS = OUT / "P8_Y5_PARENT_QLOC_1606_DELTA_W_SCORE_READINESS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1606_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1606_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1606_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1606_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1606_VALIDATION.csv"

COPY_TARGETS = {
    GRAPH_OWNER: [
        QUARANTINE / "PARENT_OWNED_GRAPH_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_owned_graph_theorem_attempt_nonclaim_1606.csv",
    ],
    EDGE_AUDIT: [
        QUARANTINE / "PARENT_OWNED_EDGE_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_owned_edge_audit_nonclaim_1606.csv",
    ],
    COMPONENT_SCHEMA: [
        QUARANTINE / "DELTA_W_COMPONENT_BOUND_SCHEMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_delta_w_component_bound_schema_nonclaim_1606.csv",
    ],
    COMPONENT_PACK: [
        QUARANTINE / "DELTA_W_COMPONENT_BOUND_PACK_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_delta_w_component_bound_pack_nonclaim_1606.csv",
    ],
    SCORE_READINESS: [
        QUARANTINE / "DELTA_W_SCORE_READINESS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_delta_w_score_readiness_nonclaim_1606.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1606.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1606_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1606_parent_owned_graph_or_Delta_w_component_bound_pack_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def graph_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "POG1606_0_target",
            "claim_piece": "parent-owned connected ordinary-matter graph",
            "formal_statement": "Every source-relevant ordinary matter sector must be linked by nonzero parent-owned action-density morphisms on one L_action line.",
            "status": "TARGET_SHARPENED",
            "what_would_close": "naturality then forces w_A=w_* across ordinary matter",
            "blocking_gap": "physical interaction connectedness has not been promoted to parent-owned morphisms",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "POG1606_1_exact_graph_lemma",
            "claim_piece": "connected parent graph collapses component weights",
            "formal_statement": "If graph G_parent is connected and each edge f has F(f) nonzero on L_action, then w_B F(f)=F(f)w_A implies all component weights equal.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "what_would_close": "Delta_w_component_vector reduces to common calibration mode",
            "blocking_gap": "edge ownership and nonzero parent map certificates are missing",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "POG1606_2_physics_not_enough",
            "claim_piece": "physical connectedness is not proof",
            "formal_statement": "QED/QCD/Yukawa/binding interactions show a useful template graph but do not by themselves prove the MTS parent action identifies source-normalization lines.",
            "status": "PHYSICAL_TEMPLATE_ONLY",
            "what_would_close": "a source path or parent theorem assigning these edges to L_action morphisms",
            "blocking_gap": "no such parent theorem/source is present",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "POG1606_3_direct_sum_countermodel",
            "claim_piece": "component-weight countermodel",
            "formal_statement": "If the parent source category splits into electron/EM/quark/QCD/nuclear/measure/current/readout components, independent Delta_w_i remain legal.",
            "status": "COUNTERMODEL_SURVIVES",
            "what_would_close": "parent-owned edges connecting every component on one action-density line",
            "blocking_gap": "component Delta_w pack must remain live",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "POG1606_4_verdict",
            "claim_piece": "parent-owned graph proof status",
            "formal_statement": "The graph lemma is exact, but no parent-owned edge certificate is imported; Delta_w cannot be theorem-zeroed in 1606.",
            "status": "PARENT_OWNED_GRAPH_NOT_DERIVED",
            "what_would_close": "source-backed parent action graph or explicit parent theorem",
            "blocking_gap": "fall back to component bound pack",
            "theorem_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def edge_audit_rows() -> list[dict[str, Any]]:
    edges = [
        ("EDGE1606_0_electron_EM", "electron/lepton to EM", "QED current edge", "PHYSICAL_TEMPLATE", False, "parent-owned L_action morphism source missing"),
        ("EDGE1606_1_EM_nuclear", "EM to nuclear binding", "Coulomb/binding contribution edge", "PHYSICAL_TEMPLATE", False, "parent material/source tensor missing"),
        ("EDGE1606_2_quark_QCD", "light quark to gluon/QCD bulk", "QCD colour edge", "PHYSICAL_TEMPLATE", False, "parent-owned QCD source-normalization edge missing"),
        ("EDGE1606_3_quark_mass", "light quark to mass/Yukawa sector", "mass-generation/source edge", "PHYSICAL_TEMPLATE", False, "mass edge not mapped to MTS parent action density"),
        ("EDGE1606_4_QCD_nuclear", "QCD bulk to nuclear binding", "bound-state edge", "PHYSICAL_TEMPLATE", False, "isotope/alloy averaged parent tensor missing"),
        ("EDGE1606_5_measure", "matter sectors to measure/Jacobian owner", "measure owner edge", "UNSIGNED_PARENT_CLAUSE", False, "species Jacobian J_A not excluded"),
        ("EDGE1606_6_current", "Hilbert source to current/readout owner", "current/readout edge", "PARTIAL_ONLY", False, "post-variation current controlled but pre-variation/readout reentry open"),
        ("EDGE1606_7_verdict", "full source-relevant graph", "all edges above", "NOT_PARENT_CERTIFIED", False, "no theorem-zero for Delta_w_component_vector"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "edge_id": edge_id,
            "edge": edge,
            "template_role": role,
            "evidence_status": evidence,
            "parent_owned": parent_owned,
            "current_blocker": blocker,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for edge_id, edge, role, evidence, parent_owned, blocker in edges
    ]


def component_schema_rows() -> list[dict[str, Any]]:
    fields = [
        ("component_id", "stable id for Delta_w component"),
        ("quantity", "delta_w_e|delta_w_EM|delta_w_q|delta_w_g|delta_w_nuc|delta_J_A|delta_c_A|zeta_A|delta_w_common"),
        ("meaning", "source/action-weight component definition"),
        ("basis", "MTS parent WEP/source basis, not DD-only proxy"),
        ("value", "finite numeric, interval, or DERIVED_ZERO; MISSING allowed only for nonclaim queue"),
        ("uncertainty", "numeric uncertainty/interval or exact theorem tag"),
        ("units", "dimensionless unless parent map proves otherwise"),
        ("sign_convention", "positive source/test/body order and field sign"),
        ("source_path", "local source artifact or URL/DOI"),
        ("source_anchor", "table/equation/row anchor"),
        ("status", "THEOREM_ZERO|SOURCE_BACKED|PROXY_NONCLAIM|MISSING"),
        ("no_bound_inversion", "must be true for claim-grade rows"),
        ("no_cancellation_rule", "forbid silent cancellation or declare covariance/source model"),
        ("valid_for_claim", "false until all components, material tensor, tau, source/readout gates pass"),
        ("claim_allowed", "false until full local branch gates pass"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "schema_id": f"DWS1606_{index}_{field}",
            "field": field,
            "required_policy": policy,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, (field, policy) in enumerate(fields)
    ]


def component_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("DWB1606_0_delta_w_common", "delta_w_common", "common calibration mode", "MISSING_OR_PROXY_NONCLAIM", "MISSING_TIME_RANGE_FRAME_SILENCE", "CBP1479_0_delta_w_common", "common mode only harmless after derivative-silence proof"),
        ("DWB1606_1_delta_w_e", "delta_w_e", "electron/lepton source-weight component", "8.948213306283e-11", "PROXY_UNIT_KERNEL_ONLY", "CBP1479_1_delta_w_e", "numeric proxy exists but tau/source/readout/product convention missing"),
        ("DWB1606_2_delta_w_EM", "delta_w_EM", "EM/Coulomb component", "MISSING_OR_PROXY_NONCLAIM", "EXTERNAL_SMOKE_NOT_PARENT_BASIS", "CBP1479_2_delta_w_EM", "needs MTS parent EM/Coulomb component map"),
        ("DWB1606_3_delta_w_q", "delta_w_q", "light-quark/sigma component", "MISSING_OR_PROXY_NONCLAIM", "MISSING_PARENT_OR_PHENOMENOLOGICAL_BASIS", "CBP1479_3_delta_w_q", "needs sourced mass-decomposition basis"),
        ("DWB1606_4_delta_w_g", "delta_w_g", "QCD/gluon/bulk binding component", "MISSING_OR_PROXY_NONCLAIM", "MISSING_PARENT_OR_PHENOMENOLOGICAL_BASIS", "CBP1479_4_delta_w_g", "bulk/common split unresolved"),
        ("DWB1606_5_delta_w_nuc", "delta_w_nuc", "nuclear binding/surface/asymmetry component", "MISSING_OR_PROXY_NONCLAIM", "EXTERNAL_SMOKE_NOT_FULL_TENSOR", "CBP1479_5_delta_w_nuc", "needs isotope/alloy-averaged nuclear binding model"),
        ("DWB1606_6_delta_J_A", "delta_J_A", "species-only measure/Jacobian residual", "MISSING_OR_PROXY_NONCLAIM", "MISSING_MEASURE_OWNER_OR_BOUND", "CBP1479_6_delta_J_A", "requires measure theorem or numeric projection"),
        ("DWB1606_7_delta_c_A", "delta_c_A", "current/source normalization residual", "MISSING_OR_PROXY_NONCLAIM", "MISSING_CURRENT_OWNER_OR_COEFFICIENT", "CBP1479_7_delta_c_A", "requires current-owner theorem or finite c_A row"),
        ("DWB1606_8_zeta_A", "zeta_A", "non-Hilbert/readout source-current residual", "MISSING_OR_PROXY_NONCLAIM", "MISSING_NONHILBERT_CURRENT_OWNER", "CBP1479_8_zeta_A", "requires J_NH definition and projection/silence proof"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": component_id,
            "quantity": quantity,
            "meaning": meaning,
            "basis": "MTS_parent_WEP_component_basis_REQUIRED",
            "value": value,
            "uncertainty": "MISSING_CLAIM_GRADE_UNCERTAINTY",
            "units": "dimensionless",
            "sign_convention": "positive means source/test component couples stronger than reference; Ti/Pt convention must be fixed before score",
            "source_path": "source-intake/microscope/branch_locked_wep/coefficients/component_delta_w_bound_pack_nonclaim_1479.csv",
            "source_anchor": anchor,
            "status": status,
            "why_not_claim": blocker,
            "no_bound_inversion": True,
            "no_cancellation_rule": "no silent cancellation; use norm/covariance only after sourced covariance matrix",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for component_id, quantity, meaning, value, status, anchor, blocker in rows
    ]


def score_readiness_rows() -> list[dict[str, Any]]:
    rows = [
        ("READY1606_0_component_vector", "all Delta_w components numeric or theorem-zero", False, "only delta_w_e proxy numeric; other components missing/proxy"),
        ("READY1606_1_material_tensor", "Ti/Pt parent material response tensor exists", False, "MAT1481_6_full_tensor is BLOCKED"),
        ("READY1606_2_tau_projection", "arena tau/source/readout projection exists", False, "tau_WEP and local projections still missing"),
        ("READY1606_3_no_cancellation", "covariance/no-cancellation rule sourced", False, "no covariance matrix/source model"),
        ("READY1606_4_parent_graph", "parent-owned connected graph theorem-zero exists", False, "POG1606 not derived"),
        ("READY1606_5_verdict", "Delta_w branch score-ready", False, "component/basis/material/tau gates open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "readiness_id": readiness_id,
            "requirement": requirement,
            "ready": ready,
            "blocker": blocker,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for readiness_id, requirement, ready, blocker in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1606_0_parent_graph",
            "acceptance_rule": "parent-owned connected graph certificate collapses Delta_w components to w_*",
            "input_state": "physical template graph exists, parent-owned edges missing",
            "runner_result": "REJECT_GRAPH_THEOREM_ZERO",
            "effect": "no no-w_A theorem-zero",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1606_1_component_pack",
            "acceptance_rule": "component pack must be fully numeric/theorem-zero with sourced material tensor, tau projection, units, signs and no-cancellation rule",
            "input_state": "component pack is source-ready but mostly missing/proxy",
            "runner_result": "COMPONENT_PACK_NOT_SCORE_READY",
            "effect": "finite/bounded route remains acquisition-ready only",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1606_2_local_policy",
            "acceptance_rule": "Newton/GR source side requires theorem-zero or bounded residual vector",
            "input_state": "neither graph-zero nor bounded vector is complete",
            "runner_result": "KEEP_LOCAL_SOURCE_BRANCH_BLOCKED",
            "effect": "no WEP/R10/PPN/clock/orbital/Newton/local-GR promotion",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1606_0_parent_edges", "parent-owned graph edges", "BLOCKED", "all audited edges are template/partial only"),
        ("CG1606_1_graph_zero", "Delta_w theorem-zero from graph", "BLOCKED", "parent graph not certified"),
        ("CG1606_2_component_pack", "Delta_w component bound pack score", "BLOCKED", "missing components, material tensor, tau, covariance"),
        ("CG1606_3_WEP", "MICROSCOPE/WEP finite score", "BLOCKED", "Delta_w_TiPt cannot be computed claim-grade"),
        ("CG1606_4_Newton_GR", "source-normalized Newton/GR", "BLOCKED", "relative source weights remain live"),
        ("CG1606_5_public_claim", "public/local claim", "BLOCKED", "private nonclaim checkpoint only"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1606_0_graph_route",
            "decision": "PARENT_OWNED_GRAPH_NOT_DERIVED",
            "reason": "the physical ordinary-matter graph is connected, but parent ownership of the action-density morphisms is missing",
            "next_action": "either source parent-owned edges or stop trying to zero Delta_w by connectedness alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1606_1_component_route",
            "decision": "DELTA_W_COMPONENT_PACK_SOURCE_READY_NOT_SCORE_READY",
            "reason": "component schema/rows exist, but most values, material tensor, tau projection and covariance are missing or proxy-only",
            "next_action": "import parent material tensor and component sensitivities, or source theorem-zero certificates per component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1606_2_next",
            "decision": "NEXT_1607_DELTA_W_MATERIAL_TENSOR_IMPORT_OR_PARENT_EDGE_CERTIFICATE",
            "reason": "material tensor is needed for finite scoring; parent edge certificate is needed for theorem-zero",
            "next_action": "source/import Ti/Pt parent material-response tensor and component sensitivities, or prove parent-owned action-density graph edges",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1607-Y5-R2FR-Delta_w-material-tensor-import-or-parent-edge-certificate.md",
            "script": "scripts/Y5_R2FR_Delta_w_material_tensor_import_or_parent_edge_certificate.py",
            "objective": "source/import Ti/Pt parent material-response tensor and component sensitivities, or prove parent-owned action-density graph edges",
            "success_condition": "claim-safe nonclaim material tensor/component sensitivity import, or parent-owned graph theorem-zero certificate; no WEP/local-GR claim until tau/source/readout gates close",
            "do_not": "do not use DD-only proxies, physical connectedness alone, closure-only zero, measured-G absorption, bound inversion, tau_eff=1, or public/local-GR claims",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1606() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1606*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    graph = read_csv(GRAPH_OWNER)
    edges = read_csv(EDGE_AUDIT)
    schema = read_csv(COMPONENT_SCHEMA)
    pack = read_csv(COMPONENT_PACK)
    readiness = read_csv(SCORE_READINESS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1606_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1606 local source paths exist"),
        ("VAL1606_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1606 source needles found"),
        ("VAL1606_2_graph_verdict", any(row["theorem_id"] == "POG1606_4_verdict" and row["status"] == "PARENT_OWNED_GRAPH_NOT_DERIVED" for row in graph), "parent-owned graph theorem remains unproved"),
        ("VAL1606_3_edges_not_parent_owned", any(row["edge_id"] == "EDGE1606_7_verdict" and row["parent_owned"].lower() == "false" for row in edges), "edge audit refuses physical-template-only promotion"),
        ("VAL1606_4_component_schema", len(schema) >= 10 and any(row["field"] == "no_cancellation_rule" for row in schema), "Delta_w component bound schema written"),
        ("VAL1606_5_component_pack_nonclaim", len(pack) >= 9 and all(row["claim_allowed"].lower() == "false" for row in pack), "component pack rows remain nonclaim"),
        ("VAL1606_6_proxy_retained", any(row["quantity"] == "delta_w_e" and row["status"] == "PROXY_UNIT_KERNEL_ONLY" for row in pack), "electron proxy retained as nonclaim, not score-ready evidence"),
        ("VAL1606_7_score_not_ready", any(row["readiness_id"] == "READY1606_5_verdict" and row["ready"].lower() == "false" for row in readiness), "Delta_w score readiness remains blocked"),
        ("VAL1606_8_runner_refuses_claims", any(row["runner_id"] == "RUN1606_0_parent_graph" and row["runner_result"] == "REJECT_GRAPH_THEOREM_ZERO" for row in runner) and any(row["runner_id"] == "RUN1606_1_component_pack" and row["runner_result"] == "COMPONENT_PACK_NOT_SCORE_READY" for row in runner), "runner refuses graph-zero and component score claims"),
        ("VAL1606_9_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" and row["status"] == "BLOCKED" for row in gates), "all 1606 claim gates remain closed"),
        ("VAL1606_10_decision_next", any(row["decision"] == "NEXT_1607_DELTA_W_MATERIAL_TENSOR_IMPORT_OR_PARENT_EDGE_CERTIFICATE" for row in decisions), "decision selects 1607 material tensor import or parent edge certificate"),
        ("VAL1606_11_csv_parse", csv_parses(generated_csvs), "all generated 1606 CSVs parse"),
        ("VAL1606_12_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1606 rows are score-ready, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1606_13_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1606_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1606_15_formalization_untouched", no_formalization_1606(), "no 1606 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1606_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1606 parent-owned matter graph or Delta_w component bound-pack validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    graph: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    readiness: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1606 - R2/fR Parent-Owned Matter Graph Or Delta_w Component Bound Pack",
                "## Verdict\n"
                "- 1606 tests whether the physical ordinary-matter interaction web can be promoted to a parent-owned action-density graph. It cannot be promoted yet.\n"
                "- The exact graph lemma remains useful: a connected parent-owned graph on one `L_action` line collapses all natural action weights to one `w_*`.\n"
                "- Physical QED/QCD/Yukawa/binding connectedness is retained as guidance only, not as proof of parent ownership.\n"
                "- The fallback `Delta_w` component pack is now explicit and source-ready, but mostly missing/proxy-only and not score-ready.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Parent-Owned Graph Theorem Attempt",
                md_table(graph, ["theorem_id", "claim_piece", "status", "what_would_close", "blocking_gap", "theorem_closed"]),
                "## Parent-Owned Edge Audit",
                md_table(edges, ["edge_id", "edge", "template_role", "evidence_status", "parent_owned", "current_blocker"]),
                "## Delta_w Component Bound Schema",
                md_table(schema, ["schema_id", "field", "required_policy"]),
                "## Delta_w Component Bound Pack",
                md_table(pack, ["component_id", "quantity", "value", "status", "why_not_claim", "source_anchor"]),
                "## Delta_w Score Readiness",
                md_table(readiness, ["readiness_id", "requirement", "ready", "blocker"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "acceptance_rule", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    graph = graph_owner_rows()
    edges = edge_audit_rows()
    schema = component_schema_rows()
    pack = component_pack_rows()
    readiness = score_readiness_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        GRAPH_OWNER,
        EDGE_AUDIT,
        COMPONENT_SCHEMA,
        COMPONENT_PACK,
        SCORE_READINESS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(GRAPH_OWNER, graph)
    write_csv(EDGE_AUDIT, edges)
    write_csv(COMPONENT_SCHEMA, schema)
    write_csv(COMPONENT_PACK, pack)
    write_csv(SCORE_READINESS, readiness)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, graph, edges, schema, pack, readiness, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
