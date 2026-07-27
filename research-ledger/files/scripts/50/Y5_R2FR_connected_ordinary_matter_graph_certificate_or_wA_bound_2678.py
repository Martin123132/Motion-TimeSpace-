from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2678"
BRANCH_ID = "Y5_R2FR_CONNECTED_ORDINARY_MATTER_GRAPH_CERTIFICATE_OR_WA_BOUND_2678"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
WEP_COEFF = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "2678-Y5-R2FR-connected-ordinary-matter-graph-certificate-or-wA-bound.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2678_SOURCE_REGISTER.csv",
    "graph_audit": RESIDUALS / "P8_Y5_R2FR_2678_CONNECTED_GRAPH_CERTIFICATE_AUDIT.csv",
    "morphism_certificate": RESIDUALS / "P8_Y5_R2FR_2678_PARENT_MORPHISM_CERTIFICATE_TEMPLATE_NONCLAIM.csv",
    "wA_bound_rows": RESIDUALS / "P8_Y5_R2FR_2678_CONNECTED_GRAPH_WA_BOUND_ROWS_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2678_GRAPH_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2678_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2678_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2678_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2678_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2678_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "microscope_graph": WEP_COEFF / "connected_ordinary_matter_graph_certificate_nonclaim_2678.csv",
    "microscope_morphisms": WEP_COEFF / "parent_morphism_certificate_template_nonclaim_2678.csv",
    "microscope_wA": WEP_COEFF / "connected_graph_wA_bound_rows_nonclaim_2678.csv",
    "source_weight": SOURCE_INTAKE / "source-weight" / "CONNECTED_GRAPH_WA_BOUND_ROWS_2678_NONCLAIM.csv",
    "local_bounds": SOURCE_INTAKE / "local_bounds" / "connected_graph_wA_bound_rows_2678_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2678_2677_AUDIT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2677_NO_SPECIES_ACTION_WEIGHT_OBJECT_LANGUAGE_AUDIT.csv",
        "required_needles": ["OL2677_3_connected_category_route", "EXACT_CONDITIONAL_THEOREM_GRAPH_OWNER_UNSIGNED", "OL2677_5_verdict"],
        "purpose": "inherits 2677 connected-category route",
    },
    {
        "source_id": "SRC2678_2677_GRAMMAR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2677_PARENT_GRAMMAR_CONTRACT_NONCLAIM.csv",
        "required_needles": ["GRM2677_2_connected_morphism_certificate", "GRM2677_4_source_label_forgetting", "GRAMMAR_NOT_PARENT_SIGNED"],
        "purpose": "imports grammar clauses required by graph certificate",
    },
    {
        "source_id": "SRC2678_2677_WA_ROWS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2677_WA_JA_BOUND_ROWS_NONCLAIM.csv",
        "required_needles": ["WJ2677_0_delta_w_AB", "WJ2677_3_connected_common_mode", "WJ2677_5_absolute_envelope"],
        "purpose": "imports w_A common-mode and bound rows",
    },
    {
        "source_id": "SRC2678_2677_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2677_NEXT_TARGET.csv",
        "required_needles": ["NEXT2677_0_selected", "connected-ordinary-matter-graph", "w_A remains nonclaim"],
        "purpose": "confirms 2678 target selection",
    },
    {
        "source_id": "SRC2678_CATEGORY_ATTEMPT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/connected_matter_category_proof_attempt_1464.csv",
        "required_needles": ["CON1464_0_target", "CON1464_1_naturality_lemma", "CON1464_2_physical_template", "CON1464_3_direct_sum_obstruction", "CON1464_5_verdict"],
        "purpose": "primary theorem attempt and obstruction",
    },
    {
        "source_id": "SRC2678_CATEGORY_SIGNING",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_connected_matter_category_signing_decision_1464.csv",
        "required_needles": ["SIGN1464_0_connected_matter_category", "naturality is exact", "REGARDS endpoints are candidates only"],
        "purpose": "records conditional-only graph/naturality decision",
    },
    {
        "source_id": "SRC2678_GRAPH_CERT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/connected_matter_graph_certificate_nonclaim_1477.csv",
        "required_needles": ["GRC1477_0_template_connectivity", "PASS_TEMPLATE_ONLY", "GRC1477_1_parent_owned_connectivity", "FAIL_NOT_PARENT_SIGNED", "GRC1477_2_action_density_line"],
        "purpose": "existing graph certificate template",
    },
    {
        "source_id": "SRC2678_GRAPH_SIGNING",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_graph_certificate_signing_decision_1465.csv",
        "required_needles": ["SIGN1465_0_graph_certificate", "all_vertices_parent_signed", "KEEP_GRAPH_TEMPLATE_NONCLAIM", "CMSM file list not acquired"],
        "purpose": "records graph template as nonclaim",
    },
    {
        "source_id": "SRC2678_SOURCE_FACTOR",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv",
        "required_needles": ["SIGN1461_0_source_factorization", "source_label_forgetting_signed", "REFUSE_DELTA_Q_ZERO_IMPORT_WRITE_CMSM_SCAFFOLD"],
        "purpose": "source-label forgetting dependency",
    },
    {
        "source_id": "SRC2678_PARENT_MEASURE_OWNER",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_parent_measure_owner_signing_decision_1463.csv",
        "required_needles": ["SIGN1463_0_parent_measure_owner", "connected_naturality_lemma", "KEEP_MEASURE_OWNER_AS_EXPLICIT_CLOSURE"],
        "purpose": "measure owner remains closure/nonclaim",
    },
    {
        "source_id": "SRC2678_COMMON_MEASURE",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_common_measure_signing_decision_1452.csv",
        "required_needles": ["SIGN1452_0_common_measure", "REFUSE_COMMON_MEASURE_ZERO_IMPORT_KEEP_JA_LEDGER"],
        "purpose": "common measure import remains refused",
    },
    {
        "source_id": "SRC2678_MINIMAL_PARENT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_minimal_parent_clause.csv",
        "required_needles": ["MPC1439_1_formal_zero", "MPC1439_4_verdict", "NOT_ADOPTED_NOT_ZERO_CERTIFIED"],
        "purpose": "full WEP zero remains conditional-only",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def graph_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "GRA2678_0_target",
            "claim_piece": "parent-owned connected ordinary-matter graph",
            "candidate_statement": "Every source-relevant ordinary sector is linked by parent-owned nonzero morphisms on the action-density/source-normalization line.",
            "current_evidence": "physical template graph is connected, but parent-owned vertices/edges/paths are unsigned",
            "current_status": "TARGET_SHARPENED_NOT_PARENT_CERTIFIED",
            "blocking_clauses": "all_vertices_parent_signed=false; all_edges_parent_signed=false; connected_paths_parent_signed=false",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_graph_certificate_nonclaim_1477.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_graph_certificate_signing_decision_1465.csv")),
                ]
            ),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "turn physical graph into a parent morphism certificate or keep w_A finite",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "GRA2678_1_naturality_lemma",
            "claim_piece": "connected graph collapses natural weights",
            "candidate_statement": "For nonzero parent-owned f:A->B, naturality w_B F(f)=F(f)w_A implies w_A=w_B; connectedness gives w_A=w_*.",
            "current_evidence": "exact conditional theorem is recorded in 1464/2677",
            "current_status": "EXACT_CONDITIONAL_LEMMA",
            "blocking_clauses": "requires nonzero parent-owned morphisms and action-density functor",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_category_proof_attempt_1464.csv")),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "use lemma only after graph certificate closes",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "GRA2678_2_physical_template",
            "claim_piece": "ordinary matter physical graph template",
            "candidate_statement": "electrons, photons, quarks, gluons, nuclear binding and atoms in Ti/Pt matter are physically coupled by EM/QCD/electroweak/bound-state maps",
            "current_evidence": "template connectivity passes only as physical guidance",
            "current_status": "PASS_TEMPLATE_ONLY_NOT_PROOF",
            "blocking_clauses": "physical couplings are not yet parent morphisms on L_action/source normalization",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_graph_certificate_nonclaim_1477.csv")),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "list vertices/edges as parent-owned or retain as template",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "GRA2678_3_direct_sum_obstruction",
            "claim_piece": "disconnected direct-sum countermodel",
            "candidate_statement": "If C_ord splits into components C_i, then independent w_i preserve naturality inside each component.",
            "current_evidence": "direct-sum obstruction survives until connectedness is parent-signed",
            "current_status": "COUNTERMODEL_SURVIVES",
            "blocking_clauses": "ordinary matter category connectedness not parent-signed",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_category_proof_attempt_1464.csv")),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "stage component-weight row until graph certificate exists",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "GRA2678_4_source_label_forgetting",
            "claim_piece": "source functor does not reintroduce labels",
            "candidate_statement": "w_A=w_* is useful only if source/readout forgets species labels before source normalization and no spurion returns afterward.",
            "current_evidence": "source factorization ledger keeps source_label_forgetting_signed=false",
            "current_status": "UNSIGNED_DEPENDENCY_RETAINED",
            "blocking_clauses": "source-label forgetting and calibration silence are not parent-signed",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv")),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "do not promote w_A common mode without source-label forgetting",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "GRA2678_5_verdict",
            "claim_piece": "connected graph certificate kills w_A",
            "candidate_statement": "connected graph + naturality + L_action owner + source-label forgetting + calibration silence implies Delta_w_AB=0",
            "current_evidence": "lemma exact, graph physical template exists, but parent graph/action line/source forgetting are unsigned",
            "current_status": "CONNECTED_GRAPH_CERTIFICATE_NOT_DERIVED",
            "blocking_clauses": "graph owner; action-density line; source-label forgetting; calibration silence; CMSM file list",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2677_NEXT_TARGET.csv")),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "build parent morphism template and keep w_A nonclaim",
            "timestamp_utc": stamp(),
        },
    ]


def morphism_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "edge_id": "MOR2678_0_electron_photon",
            "source_object": "electron",
            "target_object": "photon/EM field",
            "candidate_morphism": "EM coupling/current vertex",
            "required_parent_signature": "nonzero parent-owned morphism on ordinary action-density/source-normalization functor",
            "current_status": "PHYSICAL_TEMPLATE_NOT_PARENT_SIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_category_proof_attempt_1464.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "edge_id": "MOR2678_1_quark_gluon",
            "source_object": "quark",
            "target_object": "gluon/QCD",
            "candidate_morphism": "QCD color coupling",
            "required_parent_signature": "nonzero parent-owned morphism on ordinary action-density/source-normalization functor",
            "current_status": "PHYSICAL_TEMPLATE_NOT_PARENT_SIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_category_proof_attempt_1464.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "edge_id": "MOR2678_2_em_nuclear_binding",
            "source_object": "EM/QCD sectors",
            "target_object": "nuclear binding",
            "candidate_morphism": "bound-state/binding-energy map",
            "required_parent_signature": "parent-owned bound-state morphism with nonzero action-density map",
            "current_status": "PHYSICAL_TEMPLATE_NOT_PARENT_SIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_graph_certificate_nonclaim_1477.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "edge_id": "MOR2678_3_binding_atoms_TiPt",
            "source_object": "electron/quark/nuclear binding",
            "target_object": "Ti/Pt atoms and test-body matter",
            "candidate_morphism": "atomic/material composition map",
            "required_parent_signature": "parent-owned material object map before readout/projection",
            "current_status": "PHYSICAL_TEMPLATE_NOT_PARENT_SIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_graph_certificate_nonclaim_1477.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "edge_id": "MOR2678_4_action_density_functor",
            "source_object": "ordinary matter graph",
            "target_object": "single action-density line L_action",
            "candidate_morphism": "action-density functor F",
            "required_parent_signature": "single parent L_matter=sum_A L_A with one prefactor and no w_A slot",
            "current_status": "FAIL_LINE_OWNER_UNSIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_graph_certificate_nonclaim_1477.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "edge_id": "MOR2678_5_source_forgetting_functor",
            "source_object": "ordinary action-density/source objects",
            "target_object": "source/readout functor",
            "candidate_morphism": "species-label forgetting before source normalization",
            "required_parent_signature": "source_label_forgetting_signed=true and no post-quotient spurion re-entry",
            "current_status": "UNSIGNED_DEPENDENCY_RETAINED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def wA_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "WAB2678_0_connected_common_mode",
            "symbol": "Delta_w_AB",
            "formula": "Delta_w_AB=0 if parent graph connected and naturality/label-forgetting clauses are signed",
            "candidate_value": "ZERO_IF_CONNECTED_GRAPH_CERTIFICATE_SIGNED",
            "bound_or_scale": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2677_WA_JA_BOUND_ROWS_NONCLAIM.csv")),
            "status": "CONDITIONAL_ZERO_ONLY",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "parent-sign graph certificate before importing zero",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "WAB2678_1_direct_sum_component_weight",
            "symbol": "Delta_w_component",
            "formula": "Delta_w_component survives if C_ord decomposes into disconnected components C_i",
            "candidate_value": "MISSING_COMPONENT_GRAPH_OR_NUMERIC_WIDTH",
            "bound_or_scale": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/connected_matter_category_proof_attempt_1464.csv")),
            "status": "COUNTERMODEL_RETAINED_NONCLAIM",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "prove graph connected or bound component weight contrast",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "WAB2678_2_parent_edge_residual",
            "symbol": "epsilon_edge",
            "formula": "epsilon_edge tracks failure of physical template edges to be parent-owned nonzero morphisms",
            "candidate_value": "MISSING_PARENT_EDGE_SIGNATURES",
            "bound_or_scale": "schema",
            "units": "edge certificate",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_graph_certificate_signing_decision_1465.csv")),
            "status": "EDGE_CERTIFICATE_TEMPLATE_NONCLAIM",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "fill parent-owned vertex/edge/path signatures",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "WAB2678_3_label_reentry_residual",
            "symbol": "sigma_label_AB",
            "formula": "source/readout reintroduces material label after graph collapse",
            "candidate_value": "MISSING_SOURCE_LABEL_FORGETTING_ZERO_OR_NUMERIC_SIGMA",
            "bound_or_scale": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv")),
            "status": "LABEL_REENTRY_NONCLAIM",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive source-label forgetting or bound label reentry",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "WAB2678_4_no_cancellation",
            "symbol": "epsilon_w_graph_abs",
            "formula": "abs(epsilon_w_graph)>=abs(Delta_w_component)+abs(epsilon_edge)+abs(sigma_label_AB)",
            "candidate_value": "NOT_COMPUTED_COMPONENTS_MISSING",
            "bound_or_scale": "2.8e-15",
            "units": "dimensionless/envelope",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2677_WA_JA_BOUND_ROWS_NONCLAIM.csv")),
            "status": "NO_CANCELLATION_ENVELOPE_NOT_COMPUTED",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "score only after every graph residual is zero or bounded",
            "timestamp_utc": stamp(),
        },
    ]


def runner_results_rows(audit_rows: list[dict[str, Any]], morphism_rows: list[dict[str, Any]], bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in audit_rows:
        rows.append(
            {
                "runner_id": f"RUN2678_{row['audit_id']}",
                "target_id": row["audit_id"],
                "stage": "graph_audit",
                "has_parent_zero": row["theorem_zero"],
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(all(Path(p).exists() for p in row["source_paths"].split(";"))),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_GRAPH_CERTIFICATE_UNSIGNED",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in morphism_rows:
        rows.append(
            {
                "runner_id": f"RUN2678_{row['edge_id']}",
                "target_id": row["edge_id"],
                "stage": "morphism_certificate",
                "has_parent_zero": "false",
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(Path(row["source_path"]).exists()),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_MORPHISM_NOT_PARENT_SIGNED",
                "next_action": "parent-sign morphism or retain template",
                "timestamp_utc": stamp(),
            }
        )
    for row in bound_rows:
        rows.append(
            {
                "runner_id": f"RUN2678_{row['row_id']}",
                "target_id": row["row_id"],
                "stage": "wA_bound_row",
                "has_parent_zero": "false",
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(Path(row["source_path"]).exists()),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_WA_GRAPH_ROW_NONCLAIM",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2678_0_naturality_lemma",
            "claim": "naturality lemma is available",
            "status": "PASS_CONDITIONAL_LEMMA_ONLY",
            "blocking_rows": "graph_certificate_still_required",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2678_1_graph_certificate",
            "claim": "parent-owned graph certificate is signed",
            "status": "FAIL_PARENT_EDGES_AND_ACTION_LINE_UNSIGNED",
            "blocking_rows": "GRA2678_0_target;GRA2678_2_physical_template;MOR2678_4_action_density_functor",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2678_2_source_label_forgetting",
            "claim": "source/readout cannot reintroduce species labels",
            "status": "FAIL_SOURCE_LABEL_FORGETTING_UNSIGNED",
            "blocking_rows": "GRA2678_4_source_label_forgetting;MOR2678_5_source_forgetting_functor;WAB2678_3_label_reentry_residual",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2678_3_wA_bound",
            "claim": "w_A graph residual can be scored",
            "status": "FAIL_NONCLAIM_MISSING_COMPONENTS",
            "blocking_rows": "WAB2678_1_direct_sum_component_weight;WAB2678_2_parent_edge_residual;WAB2678_4_no_cancellation",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2678_4_local_GR",
            "claim": "local GR/PPN can use connected graph to silence w_A",
            "status": "CLAIM_BLOCKED",
            "blocking_rows": "GRA2678_5_verdict;CG2678_1_graph_certificate;CG2678_2_source_label_forgetting",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2678_0_theorem_attempt",
            "question": "Can 2678 prove connected graph collapses w_A?",
            "result": "not_yet",
            "reason": "naturality lemma is exact, but graph edges, action-density functor and source-label forgetting are not parent-signed",
            "action": "do not import Delta_w_AB=0",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2678_1_useful_result",
            "question": "What did 2678 add?",
            "result": "morphism_certificate_template",
            "reason": "physical template edges are now separated from parent-owned morphism requirements",
            "action": "use MOR2678 rows as the next closure checklist",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2678_2_next_route",
            "question": "Best next derivation target?",
            "result": "parent_action_density_line_owner",
            "reason": "without a single L_action functor, even a connected physical graph cannot kill source weights",
            "action": "select 2679 action-density line owner or edge-residual bound",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2678_0_selected",
            "kind": "selected",
            "target_doc": "2679-Y5-R2FR-parent-action-density-line-owner-or-edge-residual-bound.md",
            "target_script": "scripts/Y5_R2FR_parent_action_density_line_owner_or_edge_residual_bound_2679.py",
            "purpose": "try to prove ordinary matter maps into one parent action-density/source-normalization line, or keep graph edge/action-line residuals as explicit nonclaim bound rows",
            "acceptance_gate": "single parent L_action functor with no w_A slot, parent-owned nonzero morphisms, source-label forgetting and no-cancellation envelope",
            "forbidden_shortcuts": "treating physical connectivity as parent proof; assuming EEP/WEP; importing Delta_w=0; using classical EOM alone; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "PS2678_0_scope",
            "field": "workspace_scope",
            "value": str(ROOT),
            "status": "private_post_checkpoint_only",
            "note": "no GitHub action and no formalization-workbench writes",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2678_1_progress",
            "field": "connected_graph_route",
            "value": "exact naturality lemma retained; parent graph certificate not derived",
            "status": "improved_not_claimed",
            "note": "morphism template now separates physical guidance from proof obligations",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2678_2_next",
            "field": "next_derivation",
            "value": "parent_action_density_line_owner",
            "status": "selected",
            "note": "single L_action functor is the next root-cause target",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2678_0_graph",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["graph_audit"]),
            "destination": str(BRANCH_OUTPUTS["microscope_graph"]),
            "contents": "connected graph audit retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2678_1_morphisms",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["morphism_certificate"]),
            "destination": str(BRANCH_OUTPUTS["microscope_morphisms"]),
            "contents": "parent morphism certificate template retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2678_2_wA",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["wA_bound_rows"]),
            "destination": str(BRANCH_OUTPUTS["microscope_wA"]),
            "contents": "w_A graph-bound rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2678_3_source_weight",
            "branch": "source-weight",
            "source_table": rel_path(OUTPUTS["wA_bound_rows"]),
            "destination": str(BRANCH_OUTPUTS["source_weight"]),
            "contents": "source-weight graph/w_A rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2678_4_local_bounds",
            "branch": "local_bounds",
            "source_table": rel_path(OUTPUTS["wA_bound_rows"]),
            "destination": str(BRANCH_OUTPUTS["local_bounds"]),
            "contents": "local graph/w_A bound rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "true" and row["missing_needles"] == "" for row in rows["source_register"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_sources_exist_and_needles_found", "passed": as_bool(source_ok), "details": "all cited source paths exist and required needles are present"})

    all_nonclaim = all(row.get("valid_for_claim") == "false" for table in rows.values() for row in table)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_nonclaim_guard", "passed": as_bool(all_nonclaim), "details": "all generated rows carry valid_for_claim=false"})

    verdict_blocks = any(row["audit_id"] == "GRA2678_5_verdict" and row["current_status"] == "CONNECTED_GRAPH_CERTIFICATE_NOT_DERIVED" for row in rows["graph_audit"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_graph_verdict_blocks_claim", "passed": as_bool(verdict_blocks), "details": "connected graph theorem is not promoted"})

    lemma_present = any(row["audit_id"] == "GRA2678_1_naturality_lemma" and row["current_status"] == "EXACT_CONDITIONAL_LEMMA" for row in rows["graph_audit"])
    template_rejected = any(row["audit_id"] == "GRA2678_2_physical_template" and row["current_status"] == "PASS_TEMPLATE_ONLY_NOT_PROOF" for row in rows["graph_audit"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_lemma_template_distinction", "passed": as_bool(lemma_present and template_rejected), "details": "exact lemma is separated from physical-template nonproof"})

    morphisms_ok = len(rows["morphism_certificate"]) >= 6 and all(row["valid_for_claim"] == "false" for row in rows["morphism_certificate"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_morphism_template_complete_nonclaim", "passed": as_bool(morphisms_ok), "details": "parent morphism template rows are present and nonclaim"})

    bound_ids = {row["row_id"] for row in rows["wA_bound_rows"]}
    bounds_ok = {"WAB2678_0_connected_common_mode", "WAB2678_1_direct_sum_component_weight", "WAB2678_4_no_cancellation"}.issubset(bound_ids)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_wA_rows_complete", "passed": as_bool(bounds_ok), "details": "connected common mode, direct-sum obstruction and no-cancellation rows exist"})

    gates_ok = any(row["gate_id"] == "CG2678_4_local_GR" and row["status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and any(row["gate_id"] == "CG2678_0_naturality_lemma" and row["status"] == "PASS_CONDITIONAL_LEMMA_ONLY" for row in rows["claim_gates"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_claim_gates_correct", "passed": as_bool(gates_ok), "details": "conditional lemma is acknowledged while local-GR stays blocked"})

    runner_refuses = all(row["scored"] == "false" and row["claim_pass"] == "false" for row in rows["runner_results"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_runner_refuses_unsigned_rows", "passed": as_bool(runner_refuses), "details": "runner refuses scoring without signed graph or numeric bounds"})

    next_selected = any(row["target_id"] == "NEXT2678_0_selected" and "2679-Y5-R2FR-parent-action-density-line-owner-or-edge-residual-bound.md" in row["target_doc"] for row in rows["next_target"])
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_next_target_selected", "passed": as_bool(next_selected), "details": "next target selects parent action-density line owner"})

    parse_results = [parse_csv(path) for path in csv_paths]
    csv_ok = all(result[0] and result[1] > 0 for result in parse_results)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_csv_parse", "passed": as_bool(csv_ok), "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(csv_paths, parse_results))})

    branch_paths = [Path(row["destination"]) for row in rows["branch_copies"]]
    branch_parse = [parse_csv(path) for path in branch_paths]
    branch_ok = all(result[0] and result[1] > 0 for result in branch_parse)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_branch_copies_parse", "passed": as_bool(branch_ok), "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(branch_paths, branch_parse))})

    generated_paths = [*csv_paths, *branch_paths, DOC_PATH]
    formalization_guard = all("formalization-workbench" not in str(path) for path in generated_paths)
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_formalization_write_guard", "passed": as_bool(formalization_guard), "details": "generated path allowlist excludes formalization-workbench"})

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_pycache_absent_at_validation_time", "passed": as_bool(pycache_absent), "details": "scripts/__pycache__ absent when validation rows were produced"})

    overall = all(row["passed"] == "true" for row in out if row["validation_id"] != "VAL2678_pycache_absent_at_validation_time")
    out.append({"timestamp_utc": stamp(), "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "validation_id": "VAL2678_OVERALL", "passed": as_bool(overall), "details": "2678 keeps connected graph theorem conditional, separates physical template from parent proof, stages morphism rows, and selects action-density line owner next"})
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        f"# {CHECKPOINT} — Connected Ordinary-Matter Graph Certificate Or w_A Bound",
        "",
        "## Private Verdict",
        "",
        "2678 keeps the good part and blocks the cheat. The naturality lemma is exact: if the ordinary-matter graph is parent-owned and connected, a natural action/source weight collapses to one common mode. But the current corpus only has a physical connectivity template, not a parent-owned morphism certificate. Physical connectedness is helpful intuition; it is not yet a derivation.",
        "",
        "Therefore `Delta_w_AB=0` is not imported, WEP/local-GR stay blocked, and the next target is the single parent action-density line/functor that would turn physical edges into real parent morphisms.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["source_register"]),
        "",
        "## Graph Certificate Audit",
        "",
        markdown_table(rows["graph_audit"]),
        "",
        "## Parent Morphism Certificate Template",
        "",
        markdown_table(rows["morphism_certificate"]),
        "",
        "## w_A Graph Bound Rows",
        "",
        markdown_table(rows["wA_bound_rows"]),
        "",
        "## Runner Results",
        "",
        markdown_table(rows["runner_results"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(rows["claim_gates"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision_ledger"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next_target"]),
        "",
        "## Project Status",
        "",
        markdown_table(rows["project_status"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branch_copies"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)

    rows: dict[str, list[dict[str, Any]]] = {}
    rows["source_register"] = source_register_rows()
    rows["graph_audit"] = graph_audit_rows()
    rows["morphism_certificate"] = morphism_certificate_rows()
    rows["wA_bound_rows"] = wA_bound_rows()
    rows["runner_results"] = runner_results_rows(rows["graph_audit"], rows["morphism_certificate"], rows["wA_bound_rows"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision_ledger"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    rows["branch_copies"] = branch_copy_rows()

    for name in [
        "source_register",
        "graph_audit",
        "morphism_certificate",
        "wA_bound_rows",
        "runner_results",
        "claim_gates",
        "decision_ledger",
        "next_target",
        "project_status",
        "branch_copies",
    ]:
        write_csv(OUTPUTS[name], rows[name])

    write_csv(BRANCH_OUTPUTS["microscope_graph"], rows["graph_audit"])
    write_csv(BRANCH_OUTPUTS["microscope_morphisms"], rows["morphism_certificate"])
    write_csv(BRANCH_OUTPUTS["microscope_wA"], rows["wA_bound_rows"])
    write_csv(BRANCH_OUTPUTS["source_weight"], rows["wA_bound_rows"])
    write_csv(BRANCH_OUTPUTS["local_bounds"], rows["wA_bound_rows"])

    csv_paths = [OUTPUTS[name] for name in OUTPUTS if name != "validation"]
    rows["validation"] = validation_rows(rows, csv_paths)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
