from __future__ import annotations

import csv
import math
import sys
from collections import deque
from pathlib import Path
from typing import Any


COMMON_FLAGS = (
    "source_signed",
    "units_signed",
    "same_branch_signed",
    "no_cancellation_guard",
)

ZERO_FLAGS = (
    "parent_matter_category_signed",
    "single_action_density_line_signed",
    "common_measure_normalization_signed",
    "connected_ordinary_matter_category_signed",
    "total_Hilbert_source_functor_signed",
    "parent_generator_exhausted_signed",
    "edge_ownership_certified_signed",
    "edge_nonzero_certified_signed",
    "species_label_forgetful_signed",
    "hidden_marker_absent_signed",
    "readout_no_reentry_signed",
    "constant_sector_universal_signed",
    "common_calibration_removed_signed",
    "variation_before_readout_signed",
    "no_species_only_jacobian_signed",
    "no_post_variation_selector_signed",
    "no_bound_as_source_signed",
    "no_G_or_GM_absorption_signed",
)

BOUND_FIELDS = (
    "R_graph_disconnect_abs",
    "R_edge_ownership_abs",
    "R_generator_exhaustion_abs",
    "R_hidden_marker_abs",
    "R_readout_reentry_abs",
    "R_constant_sector_abs",
    "R_action_line_abs",
    "P_kappaA_delta_w_abs",
    "P_density_kappaA_abs",
    "P_kappaA_qbar_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_kappaA_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BOUND_AS_SOURCE",
    "CANCEL_UNKNOWN_COMPONENTS",
    "COMMON_MODE_HIDES_RELATIVE_WEIGHT",
    "EDGE_BY_LABEL_ONLY",
    "G_ABSORPTION",
    "GM_ABSORPTION",
    "GRAPH_CONNECTED_BY_DECLARATION",
    "HIDDEN_MARKER_FIT",
    "KAPPA_A_BY_DECLARATION",
    "MEASURED_GM_AS_SOURCE",
    "NOHOM_BY_DECLARATION",
    "POST_VARIATION_SELECTOR",
    "READOUT_MASK_AS_SOURCE",
    "SOURCE_ONLY_WEIGHT_ASSERTED_ZERO",
    "SPECIES_LABEL_FIT",
    "UNIT_RESCALING",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed", "derived"}


def missing_text(value: Any) -> bool:
    text = str(value or "").strip()
    return not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE", "NOT_COMPUTED"}


def parse_float(value: Any) -> float | None:
    if missing_text(value):
        return None
    try:
        number = float(str(value).strip())
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def fmt(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def source_ok(row: dict[str, Any]) -> bool:
    source_path = str(row.get("source_path", "")).strip()
    return bool(source_path) and not missing_text(source_path) and Path(source_path).exists()


def forbidden_source_used(row: dict[str, Any]) -> bool:
    text = " ".join(
        str(row.get(field, ""))
        for field in ("row_id", "route_type", "route", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    normalized = text.replace(" ", "_").replace("-", "_")
    return any(token in normalized for token in FORBIDDEN_SOURCE_TOKENS)


def parse_items(value: Any) -> list[str]:
    text = str(value or "").strip()
    if missing_text(text):
        return []
    raw_parts = text.replace("|", ";").replace(",", ";").split(";")
    return [part.strip() for part in raw_parts if part.strip()]


def parse_edges(value: Any) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    for raw in parse_items(value):
        if "->" in raw:
            left, right = raw.split("->", 1)
        elif "-" in raw:
            left, right = raw.split("-", 1)
        else:
            continue
        a = left.strip()
        b = right.strip()
        if a and b and a != b:
            edges.append((a, b))
    return edges


def graph_status(row: dict[str, Any]) -> dict[str, Any]:
    objects = parse_items(row.get("objects"))
    edges = parse_edges(row.get("edges"))
    if not objects:
        return {
            "graph_object_count": 0,
            "graph_edge_count": len(edges),
            "graph_component_count": "MISSING_GRAPH_OBJECTS",
            "graph_connected": False,
            "graph_missing": "MISSING_objects",
        }
    object_set = set(objects)
    unknown_edges = sorted({node for edge in edges for node in edge if node not in object_set})
    adjacency = {node: set() for node in objects}
    for a, b in edges:
        if a in object_set and b in object_set:
            adjacency[a].add(b)
            adjacency[b].add(a)
    seen: set[str] = set()
    components = 0
    for start in objects:
        if start in seen:
            continue
        components += 1
        queue: deque[str] = deque([start])
        seen.add(start)
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
    missing: list[str] = []
    if unknown_edges:
        missing.append("UNKNOWN_EDGE_NODE_" + "_".join(unknown_edges))
    if not edges:
        missing.append("MISSING_edges")
    if components != 1:
        missing.append(f"GRAPH_NOT_CONNECTED_components_{components}")
    return {
        "graph_object_count": len(objects),
        "graph_edge_count": len(edges),
        "graph_component_count": components,
        "graph_connected": components == 1 and not unknown_edges and bool(edges),
        "graph_missing": ";".join(missing),
    }


def base_missing(row: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    if not source_ok(row):
        missing.append("MISSING_source_path")
    for flag in COMMON_FLAGS:
        if not bool_text(row.get(flag)):
            missing.append(f"MISSING_{flag}")
    return missing


def nonnegative(row: dict[str, Any], field: str, missing: list[str]) -> float | None:
    value = parse_float(row.get(field))
    if value is None:
        missing.append(f"MISSING_{field}")
        return None
    if value < 0.0:
        missing.append(f"NEGATIVE_{field}")
        return None
    return value


def projection_outputs(density: float | None, P: float | None, Qbar: float | None, K: float | None, tau: float | None) -> dict[str, float | None]:
    if None in (density, P, Qbar, K, tau):
        return {"qbar": None, "alpha": None, "BY5": None}
    qbar = P * density
    return {"qbar": qbar, "alpha": K * Qbar * qbar, "BY5": tau * qbar}


def empty_numbers() -> dict[str, str]:
    return {
        "kappaA_source_rel_abs": "MISSING_NUMERIC_VALUE",
        "delta_w_species_abs": "MISSING_NUMERIC_VALUE",
        "density_qbasic_feed_abs": "MISSING_NUMERIC_VALUE",
        "qbar_XT_kappaA_feed_abs": "MISSING_NUMERIC_VALUE",
        "alpha_source_abs": "MISSING_NUMERIC_VALUE",
        "BY5_kappaA_feed_abs": "MISSING_NUMERIC_VALUE",
    }


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        "graph_object_count": "MISSING_GRAPH_OBJECTS",
        "graph_edge_count": "MISSING_GRAPH_EDGES",
        "graph_component_count": "MISSING_GRAPH_COMPONENTS",
        "graph_connected": False,
        **empty_numbers(),
        "kappaA_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def evaluate_graph(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    graph = graph_status(row)
    if graph["graph_missing"]:
        missing.extend(str(graph["graph_missing"]).split(";"))
    passed = not missing and bool(graph["graph_connected"])
    return {
        **graph,
        **empty_numbers(),
        "kappaA_status": "CONNECTED_GRAPH_CERTIFICATE_READY" if passed else "CONNECTED_GRAPH_CERTIFICATE_BLOCKED",
        "route_pass": passed,
        "runner_status": "GRAPH_CERTIFICATE_PASS_NONCLAIM" if passed else "BLOCKED_GRAPH_CERTIFICATE",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_nohom_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    graph = graph_status(row)
    if graph["graph_missing"]:
        missing.extend(str(graph["graph_missing"]).split(";"))
    for field in ZERO_FLAGS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing and bool(graph["graph_connected"])
    zero = "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE"
    return {
        **graph,
        "kappaA_source_rel_abs": zero,
        "delta_w_species_abs": zero,
        "density_qbasic_feed_abs": zero,
        "qbar_XT_kappaA_feed_abs": zero,
        "alpha_source_abs": zero,
        "BY5_kappaA_feed_abs": zero,
        "kappaA_status": "PARENT_MATTER_NOHOM_KAPPAA_ZERO_SIGNED" if passed else "PARENT_MATTER_NOHOM_KAPPAA_ZERO_UNSIGNED",
        "route_pass": passed,
        "runner_status": "NOHOM_KAPPAA_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_NOHOM_KAPPAA_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_kappaA_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in BOUND_FIELDS}
    kappa_residual = None
    delta_w = None
    density = None
    projection = {"qbar": None, "alpha": None, "BY5": None}
    if not missing:
        kappa_residual = (
            values["R_graph_disconnect_abs"]
            + values["R_edge_ownership_abs"]
            + values["R_generator_exhaustion_abs"]
            + values["R_hidden_marker_abs"]
            + values["R_readout_reentry_abs"]
            + values["R_constant_sector_abs"]
            + values["R_action_line_abs"]
        )
        delta_w = values["P_kappaA_delta_w_abs"] * kappa_residual
        density = values["P_density_kappaA_abs"] * kappa_residual + delta_w
        projection = projection_outputs(
            density,
            values["P_kappaA_qbar_abs"],
            values["Qbar_source_XH_bound_abs"],
            values["K_source_abs"],
            values["tau_BY5_kappaA_abs"],
        )
    passed = not missing
    return {
        "graph_object_count": "NOT_GRAPH_ROUTE",
        "graph_edge_count": "NOT_GRAPH_ROUTE",
        "graph_component_count": "NOT_GRAPH_ROUTE",
        "graph_connected": "NOT_GRAPH_ROUTE",
        "kappaA_source_rel_abs": fmt(kappa_residual),
        "delta_w_species_abs": fmt(delta_w),
        "density_qbasic_feed_abs": fmt(density),
        "qbar_XT_kappaA_feed_abs": fmt(projection["qbar"]),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_kappaA_feed_abs": fmt(projection["BY5"]),
        "kappaA_status": "FINITE_KAPPAA_HIDDEN_MARKER_ROW_READY" if passed else "FINITE_KAPPAA_HIDDEN_MARKER_ROW_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "KAPPAA_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_KAPPAA_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_KAPPAA_ROW"
    route_type = str(row.get("route_type", "")).strip()
    route = row.get("route", "")
    if forbidden_source_used(row):
        return forbidden_result(row_id, route_type, route)
    if route_type == "graph_certificate":
        result = evaluate_graph(row)
    elif route_type == "nohom_kappaA_zero":
        result = evaluate_nohom_zero(row)
    elif route_type == "kappaA_bound":
        result = evaluate_kappaA_bound(row)
    else:
        result = {
            "graph_object_count": "UNKNOWN_ROUTE_TYPE",
            "graph_edge_count": "UNKNOWN_ROUTE_TYPE",
            "graph_component_count": "UNKNOWN_ROUTE_TYPE",
            "graph_connected": False,
            **empty_numbers(),
            "kappaA_status": "UNKNOWN_ROUTE_TYPE",
            "route_pass": False,
            "runner_status": "FAILED_UNKNOWN_ROUTE_TYPE",
            "missing_for_claim": "UNKNOWN_ROUTE_TYPE",
        }
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        **result,
        "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
    }


def run(input_path: Path, output_path: Path) -> None:
    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    outputs = [evaluate_row(row) for row in rows]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(field for row in outputs for field in row))
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(outputs)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: parent_matter_nohom_kappaA_runner.py INPUT.csv OUTPUT.csv")
    run(Path(sys.argv[1]), Path(sys.argv[2]))
