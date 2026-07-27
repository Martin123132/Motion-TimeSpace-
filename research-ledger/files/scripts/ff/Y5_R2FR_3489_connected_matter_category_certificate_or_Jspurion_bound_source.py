from __future__ import annotations

import csv
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3489-Y5-R2FR-connected-matter-category-certificate-or-Jspurion-bound-source.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3489": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3488": {
        "path": ROOT / "3488-Y5-R2FR-no-source-only-matter-grammar-or-finite-Jq-coefficient-row.md",
        "role": "3488 no-source theorem handoff",
    },
    "connected_1464": {
        "path": ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients" / "connected_matter_category_proof_attempt_1464.csv",
        "role": "connected ordinary matter category proof attempt",
    },
    "measure_1452": {
        "path": ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients" / "common_measure_current_theorem_attempt_1452.csv",
        "role": "common measure/current theorem attempt",
    },
    "source_factor_1461": {
        "path": ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients" / "parent_source_factorization_no_relative_label_attempt_1461.csv",
        "role": "source-label forgetting/factorization attempt",
    },
    "finite_3488": {
        "path": OUT / "P8_Y5_R2FR_3488_FINITE_JSPURION_COEFFICIENT_ROWS.csv",
        "role": "finite J_spurion fallback coefficients",
    },
    "gates_3488": {
        "path": OUT / "P8_Y5_R2FR_3488_GATES.csv",
        "role": "3488 grammar gates",
    },
    "matrix_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv",
        "role": "WEP/clock matrix with WEP empirical bounds",
    },
    "bridge_3487": {
        "path": OUT / "P8_Y5_R2FR_3487_PARENT_TO_DD_BRIDGE_DERIVATION.csv",
        "role": "S_E^q bridge equation",
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(meta["path"]),
            "exists": str(Path(meta["path"]).exists()),
            "role": meta["role"],
            "valid_for_claim": "False",
        }
        for source_id, meta in SOURCES.items()
    ]


def graph_nodes() -> list[dict[str, Any]]:
    nodes = [
        ("electron", "charged_lepton", "ordinary matter constituent"),
        ("photon", "gauge_boson", "EM connector and readout field"),
        ("up_quark", "quark", "nucleon constituent"),
        ("down_quark", "quark", "nucleon constituent"),
        ("gluon", "gauge_boson", "QCD connector"),
        ("proton", "baryon", "bound state of quarks/gluons"),
        ("neutron", "baryon", "bound state of quarks/gluons"),
        ("nucleus", "bound_state", "ordinary nuclear source/test core"),
        ("atom", "bound_state", "neutral ordinary matter unit"),
        ("bulk_matter", "composite", "Earth/test-body matter aggregate"),
    ]
    return [
        {
            "node_id": node_id,
            "node_type": node_type,
            "meaning": meaning,
            "parent_owned_now": "False",
            "template_status": "PHYSICAL_TEMPLATE_NODE_NONCLAIM",
            "valid_for_claim": "False",
        }
        for node_id, node_type, meaning in nodes
    ]


def graph_edges() -> list[dict[str, Any]]:
    edges = [
        ("electron", "photon", "EM_vertex", "charged leptons couple to EM field"),
        ("up_quark", "photon", "EM_vertex", "up quark couples to EM field"),
        ("down_quark", "photon", "EM_vertex", "down quark couples to EM field"),
        ("up_quark", "gluon", "QCD_vertex", "quark couples to gluon field"),
        ("down_quark", "gluon", "QCD_vertex", "quark couples to gluon field"),
        ("up_quark", "proton", "bound_state_map", "proton contains up/down quarks and gluons"),
        ("down_quark", "proton", "bound_state_map", "proton contains up/down quarks and gluons"),
        ("up_quark", "neutron", "bound_state_map", "neutron contains up/down quarks and gluons"),
        ("down_quark", "neutron", "bound_state_map", "neutron contains up/down quarks and gluons"),
        ("proton", "nucleus", "nuclear_binding", "nucleus contains protons"),
        ("neutron", "nucleus", "nuclear_binding", "nucleus contains neutrons"),
        ("nucleus", "atom", "atomic_binding", "atom contains nucleus"),
        ("electron", "atom", "atomic_binding", "atom contains electrons"),
        ("atom", "bulk_matter", "composition_sum", "bulk ordinary matter is atom/material composition"),
    ]
    return [
        {
            "edge_id": f"EDGE3489_{index}",
            "source_node": source,
            "target_node": target,
            "morphism_type": edge_type,
            "meaning": meaning,
            "nonzero_template_edge": "True",
            "parent_owned_now": "False",
            "source_path": str(SOURCES["connected_1464"]["path"]),
            "valid_for_claim": "False",
        }
        for index, (source, target, edge_type, meaning) in enumerate(edges)
    ]


def component_rows(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    adjacency: dict[str, set[str]] = {node["node_id"]: set() for node in nodes}
    for edge in edges:
        adjacency[edge["source_node"]].add(edge["target_node"])
        adjacency[edge["target_node"]].add(edge["source_node"])
    seen: set[str] = set()
    components: list[list[str]] = []
    for node in adjacency:
        if node in seen:
            continue
        queue: deque[str] = deque([node])
        seen.add(node)
        component: list[str] = []
        while queue:
            current = queue.popleft()
            component.append(current)
            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        components.append(sorted(component))
    return [
        {
            "component_id": f"COMP3489_{index}",
            "node_count": len(component),
            "nodes": ";".join(component),
            "template_connected_component": "True",
            "parent_owned_connected_component": "False",
            "claim_status": "TEMPLATE_CONNECTED_PARENT_GRAPH_UNSIGNED",
            "valid_for_claim": "False",
        }
        for index, component in enumerate(components)
    ]


def certificate_rows(components: list[dict[str, Any]]) -> list[dict[str, Any]]:
    template_connected = len(components) == 1
    return [
        {
            "certificate_id": "CERT3489_0_template_graph_connected",
            "statement": "The physical ordinary-matter template graph is connected.",
            "evidence": f"component_count={len(components)}",
            "passed": str(template_connected),
            "claim_effect": "supports the connected-category premise shape only",
            "valid_for_claim": "False",
        },
        {
            "certificate_id": "CERT3489_1_parent_graph_owner",
            "statement": "The connected graph is supplied as a parent-owned matter category.",
            "evidence": "1464 status says physical template is guidance, not parent proof",
            "passed": "False",
            "claim_effect": "blocks theorem-zero for epsilon_J_spurion",
            "valid_for_claim": "False",
        },
        {
            "certificate_id": "CERT3489_2_species_blind_measure",
            "statement": "The parent action supplies one species-blind measure/current normalization.",
            "evidence": "1452 common measure/current theorem remains unsigned",
            "passed": "False",
            "claim_effect": "blocks theorem-zero for epsilon_species_measure",
            "valid_for_claim": "False",
        },
        {
            "certificate_id": "CERT3489_3_source_label_forgetting",
            "statement": "Source/readout functor forgets labels before source normalization.",
            "evidence": "1461 says label-forgetting/no-relative-slot clause is not reduced",
            "passed": "False",
            "claim_effect": "blocks theorem-zero for epsilon_source_reentry",
            "valid_for_claim": "False",
        },
    ]


def product_bound_rows() -> list[dict[str, Any]]:
    matrix = read_csv(SOURCES["matrix_3475"]["path"])
    wep_rows = [row for row in matrix if row["row_type"] == "WEP_material_difference"]
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(wep_rows):
        rows.append(
            {
                "product_bound_id": f"JSPB3489_{index}_{row['aug_row_id']}",
                "arena": row["arena"],
                "observable_row": row["aug_row_id"],
                "product_symbol": "abs(S_E^q) * abs(Delta_epsilon_Jspurion_AB)",
                "bound_value": row["bound"],
                "bound_units": row["bound_units"],
                "derivation": "A residual source/species prefactor contrast adds to the WEP/source product; empirical eta bound limits the product, not isolated epsilon_J_spurion.",
                "source_path": row["source_path"],
                "isolates_epsilon": "False",
                "missing_for_isolation": "parent-owned lower bound on abs(S_E^q) or theorem-zero for source amplitude",
                "valid_for_claim": "False",
            }
        )
    return rows


def finite_update_rows(product_bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    finite = read_csv(SOURCES["finite_3488"]["path"])
    rows: list[dict[str, Any]] = []
    for row in finite:
        if row["symbol"] == "epsilon_J_spurion":
            rows.append(
                {
                    "coefficient_id": row["coefficient_id"],
                    "symbol": row["symbol"],
                    "old_status": row["current_value"],
                    "new_status": "PRODUCT_BOUNDED_NOT_ISOLATED",
                    "bound_source": ";".join(bound["product_bound_id"] for bound in product_bounds),
                    "meaning": "epsilon_J_spurion is not numeric, but its source product is now tied to WEP eta bounds.",
                    "valid_for_claim": "False",
                }
            )
        else:
            rows.append(
                {
                    "coefficient_id": row["coefficient_id"],
                    "symbol": row["symbol"],
                    "old_status": row["current_value"],
                    "new_status": "STILL_MISSING_THEOREM_ZERO_OR_SOURCE_BOUND",
                    "bound_source": "",
                    "meaning": "not bounded by the current WEP source-product interface in this checkpoint",
                    "valid_for_claim": "False",
                }
            )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM3489_0_template_connectedness",
            "statement": "The ordinary-matter physical template graph containing quarks, gluons, photons, electrons, nuclei, atoms, and bulk matter is connected.",
            "proof": "The edge list links all nodes through EM, QCD, bound-state, atomic, and composition morphism templates; the graph traversal returns one component.",
            "result": "connectedness premise is structurally plausible but parent-owner unsigned",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3489_1_parent_certificate_failure",
            "statement": "Template connectedness does not sign the parent matter category.",
            "proof": "1464 explicitly labels the interaction web as physical guidance and retains graph-owner/source-label-forgetting/calibration blockers.",
            "result": "epsilon_J_spurion theorem-zero is not claimable yet",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3489_2_product_bound",
            "statement": "Even without isolated epsilon_J_spurion, WEP rows source a finite product bound on abs(S_E^q) times the spurion contrast.",
            "proof": "A source/species prefactor residual enters eta as a product with the common Earth source leg; measured eta bounds constrain that product.",
            "result": "J_spurion residual moves from missing-only to PRODUCT_BOUNDED_NOT_ISOLATED",
            "valid_for_claim": "False",
        },
    ]


def gate_rows(certificates: list[dict[str, Any]], product_bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3489_0_template_connected",
            "requirement": "ordinary matter template graph is connected",
            "passed": next(row["passed"] for row in certificates if row["certificate_id"] == "CERT3489_0_template_graph_connected"),
            "evidence": "component scan",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3489_1_parent_graph_owned",
            "requirement": "parent action owns the connected graph",
            "passed": "False",
            "evidence": "1464 parent-owned graph not constructed",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3489_2_species_blind_measure_owned",
            "requirement": "parent action owns species-blind measure/current normalization",
            "passed": "False",
            "evidence": "1452 theorem unsigned; Jacobian/current countermodels survive",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3489_3_source_label_forgetting_owned",
            "requirement": "source labels cannot reenter after quotient/readout",
            "passed": "False",
            "evidence": "1461 label-forgetting/no-relative-slot clause not reduced",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3489_4_Jspurion_product_bound",
            "requirement": "finite source-backed product bound rows exist for J_spurion",
            "passed": str(len(product_bounds) > 0),
            "evidence": f"product_bound_rows={len(product_bounds)}",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3489_0_connectedness",
            "decision": "Template connectedness is established; parent-owned connectedness is not.",
            "rationale": "The graph is connected, but 1464 says the graph has not been supplied by the parent action.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3489_1_Jspurion_status",
            "decision": "Upgrade epsilon_J_spurion from missing-only to product-bounded-not-isolated.",
            "rationale": "WEP eta rows bound abs(S_E^q)*abs(Delta epsilon_Jspurion), but no source-amplitude lower bound isolates epsilon_Jspurion.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3489_2_best_next_attack",
            "decision": "Attack species-blind measure/current ownership next, because it blocks both epsilon_species_measure and parent graph signing.",
            "rationale": "1452 has explicit quantum-measure and current-owner routes plus surviving countermodels; this is the next load-bearing residual.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3490-Y5-R2FR-species-blind-measure-current-owner-or-product-bound-upgrade.md",
            "next_script": "scripts/Y5_R2FR_3490_species_blind_measure_current_owner_or_product_bound_upgrade.py",
            "objective": "Try to derive the species-blind parent measure/current owner; if not, upgrade epsilon_species_measure and current-rescaling residuals into finite product-bound rows.",
            "success_gate": "common measure/current theorem signed, or epsilon_species_measure/J_nonH/c_A current residuals get source-backed product bounds",
            "forbidden_shortcuts": "using classical EOM equivalence as source proof; deleting species Jacobian countermodel; isolating epsilon without source amplitude",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(outputs: dict[str, Path], components: list[dict[str, Any]], product_bounds: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append({"check_id": "VAL3489_0_sources_exist", "passed": all(Path(meta["path"]).exists() for meta in SOURCES.values()), "detail": "all cited local sources exist", "valid_for_claim": "False"})
    parse_ok = True
    details = []
    for name, path in outputs.items():
        try:
            parsed = read_csv(path)
            details.append(f"{name}:{len(parsed)}")
        except Exception as exc:
            parse_ok = False
            details.append(f"{name}:ERROR:{exc}")
    rows.append({"check_id": "VAL3489_1_csv_parse", "passed": parse_ok, "detail": "; ".join(details), "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3489_2_template_graph_connected", "passed": len(components) == 1, "detail": f"components={len(components)}", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3489_3_product_bounds_exist", "passed": len(product_bounds) >= 2, "detail": f"product_bounds={len(product_bounds)}", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3489_4_parent_claim_blocked", "passed": any(row["passed"] == "False" and row["blocks_claim"] == "True" for row in gates), "detail": "parent graph/measure/source-label gates block claim", "valid_for_claim": "False"})
    all_rows: list[dict[str, str]] = []
    for path in outputs.values():
        all_rows.extend(read_csv(path))
    rows.append({"check_id": "VAL3489_5_no_claim", "passed": all(row.get("valid_for_claim") == "False" for row in all_rows), "detail": "all generated rows valid_for_claim=false", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3489_6_no_formalization_outputs", "passed": all(FORMALIZATION not in path.parents for path in outputs.values()), "detail": "outputs are under post-checkpoint-work/source-intake only", "valid_for_claim": "False"})
    passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append({"check_id": "VAL3489_SUMMARY", "passed": passed, "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return rows


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, sep] + body)


def write_doc(
    components: list[dict[str, Any]],
    certificates: list[dict[str, Any]],
    product_bounds: list[dict[str, Any]],
    finite_updates: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3489: Connected Matter Category Certificate Or `J_spurion` Bound Source",
                "",
                "## Current Verdict",
                "- **Template result:** the ordinary-matter physical interaction graph is connected.",
                "- **Claim guard:** template connectedness is not parent-owned connectedness; 1464/1452/1461 still block theorem-zero.",
                "- **Concrete progress:** `epsilon_J_spurion` is upgraded from missing-only to product-bounded-not-isolated via WEP source-product rows.",
                "- **No claim:** no local-GR/source-coupling pass is claimed.",
                "",
                "## Graph Components",
                md_table(components, ["component_id", "node_count", "nodes", "template_connected_component", "parent_owned_connected_component", "claim_status", "valid_for_claim"]),
                "",
                "## Certificates",
                md_table(certificates, ["certificate_id", "statement", "evidence", "passed", "claim_effect", "valid_for_claim"]),
                "",
                "## J Spurion Product Bounds",
                md_table(product_bounds, ["product_bound_id", "arena", "observable_row", "product_symbol", "bound_value", "bound_units", "isolates_epsilon", "missing_for_isolation", "valid_for_claim"]),
                "",
                "## Finite Coefficient Updates",
                md_table(finite_updates, ["coefficient_id", "symbol", "old_status", "new_status", "bound_source", "meaning", "valid_for_claim"]),
                "",
                "## Theorems",
                md_table(theorems, ["theorem_id", "statement", "proof", "result", "valid_for_claim"]),
                "",
                "## Gates",
                md_table(gates, ["gate_id", "requirement", "passed", "evidence", "blocks_claim", "valid_for_claim"]),
                "",
                "## Decisions",
                md_table(decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"_Generated: {now()}_",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    nodes = graph_nodes()
    edges = graph_edges()
    components = component_rows(nodes, edges)
    certificates = certificate_rows(components)
    product_bounds = product_bound_rows()
    finite_updates = finite_update_rows(product_bounds)
    theorems = theorem_rows()
    gates = gate_rows(certificates, product_bounds)
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3489_SOURCE_REGISTER.csv",
        "graph_nodes": OUT / "P8_Y5_R2FR_3489_MATTER_GRAPH_NODES.csv",
        "graph_edges": OUT / "P8_Y5_R2FR_3489_MATTER_GRAPH_EDGES.csv",
        "components": OUT / "P8_Y5_R2FR_3489_MATTER_GRAPH_COMPONENTS.csv",
        "certificates": OUT / "P8_Y5_R2FR_3489_CERTIFICATE_LEDGER.csv",
        "product_bounds": OUT / "P8_Y5_R2FR_3489_JSPURION_PRODUCT_BOUND_ROWS.csv",
        "finite_updates": OUT / "P8_Y5_R2FR_3489_FINITE_COEFFICIENT_UPDATES.csv",
        "theorems": OUT / "P8_Y5_R2FR_3489_THEOREM_LEDGER.csv",
        "gates": OUT / "P8_Y5_R2FR_3489_GATES.csv",
        "decisions": OUT / "P8_Y5_R2FR_3489_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3489_NEXT_TARGET.csv",
    }
    write_csv(outputs["source_register"], source_register(), ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["graph_nodes"], nodes, ["node_id", "node_type", "meaning", "parent_owned_now", "template_status", "valid_for_claim"])
    write_csv(outputs["graph_edges"], edges, ["edge_id", "source_node", "target_node", "morphism_type", "meaning", "nonzero_template_edge", "parent_owned_now", "source_path", "valid_for_claim"])
    write_csv(outputs["components"], components, ["component_id", "node_count", "nodes", "template_connected_component", "parent_owned_connected_component", "claim_status", "valid_for_claim"])
    write_csv(outputs["certificates"], certificates, ["certificate_id", "statement", "evidence", "passed", "claim_effect", "valid_for_claim"])
    write_csv(outputs["product_bounds"], product_bounds, ["product_bound_id", "arena", "observable_row", "product_symbol", "bound_value", "bound_units", "derivation", "source_path", "isolates_epsilon", "missing_for_isolation", "valid_for_claim"])
    write_csv(outputs["finite_updates"], finite_updates, ["coefficient_id", "symbol", "old_status", "new_status", "bound_source", "meaning", "valid_for_claim"])
    write_csv(outputs["theorems"], theorems, ["theorem_id", "statement", "proof", "result", "valid_for_claim"])
    write_csv(outputs["gates"], gates, ["gate_id", "requirement", "passed", "evidence", "blocks_claim", "valid_for_claim"])
    write_csv(outputs["decisions"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, components, product_bounds, gates)
    validation_path = OUT / "P8_Y5_BRR545_3489_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(components, certificates, product_bounds, finite_updates, theorems, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
