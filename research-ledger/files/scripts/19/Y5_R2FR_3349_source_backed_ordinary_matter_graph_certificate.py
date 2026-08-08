from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3349-Y5-R2FR-source-backed-ordinary-matter-graph-certificate-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3349_0_3348_doc", ROOT / "3348-Y5-R2FR-source-shadow-response-basis-or-zero-under-AX1090.md", "3348 response-basis fork"),
    ("LSRC3349_1_3348_theorem", OUT / "P8_Y5_R2FR_3348_RESPONSE_BASIS_THEOREM.csv", "3348 R_AB theorem rows"),
    ("LSRC3349_2_3348_graph", OUT / "P8_Y5_R2FR_3348_HILBERT_GRAPH_COLLAPSE.csv", "3348 graph-collapse rows"),
    ("LSRC3349_3_2616_graph_attempt", OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv", "2616 private standard matter graph"),
    ("LSRC3349_4_2616_connectivity", OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv", "2616 graph theorem"),
    ("LSRC3349_5_3345_weight_collapse", OUT / "P8_Y5_R2FR_3345_SOURCE_WEIGHT_COLLAPSE_THEOREM.csv", "3345 source-weight collapse"),
    ("LSRC3349_6_3346_allowed_args", OUT / "P8_Y5_R2FR_3346_ALLOWED_ARGUMENT_INVENTORY.csv", "3346 allowed parent action arguments"),
]

WEB_SOURCES = [
    {
        "web_source_id": "WEB3349_0_hilbert_metric_variation",
        "title": "Hilbert stress-energy from metric variation / action source owner",
        "url": "https://arxiv.org/abs/2211.03092",
        "source_type": "field_theory_reference",
        "usage": "anchors the Hilbert-source convention T_H as an action/metric variation object",
        "confidence": "source_anchor_not_full_parent_signature",
        "valid_for_claim": "false",
    },
    {
        "web_source_id": "WEB3349_1_em_stress_exchange",
        "title": "Electromagnetic stress-energy exchange with charged matter / Lorentz-force density",
        "url": "https://arxiv.org/abs/1404.5250",
        "source_type": "classical_field_theory_reference",
        "usage": "anchors the charged-matter--EM exchange edge used in the ordinary matter graph",
        "confidence": "source_anchor_not_material_specific",
        "valid_for_claim": "false",
    },
    {
        "web_source_id": "WEB3349_2_pdg_standard_model",
        "title": "Particle Data Group Review: The Standard Model",
        "url": "https://pdg.lbl.gov/2023/reviews/rpp2023-rev-standard-model.pdf",
        "source_type": "authoritative_review",
        "usage": "anchors the ordinary particle/gauge-interaction setting for charged leptons, quarks, and gauge fields",
        "confidence": "source_anchor",
        "valid_for_claim": "false",
    },
    {
        "web_source_id": "WEB3349_3_pdg_qcd",
        "title": "Particle Data Group Review: Quantum Chromodynamics",
        "url": "https://pdg.lbl.gov/2023/reviews/rpp2023-rev-qcd.pdf",
        "source_type": "authoritative_review",
        "usage": "anchors the quark/gluon strong-interaction and nuclear-binding edge family",
        "confidence": "source_anchor_not_nuclear_model",
        "valid_for_claim": "false",
    },
    {
        "web_source_id": "WEB3349_4_nist_atomic_weights",
        "title": "NIST Atomic Weights and Isotopic Compositions",
        "url": "https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl",
        "source_type": "measurement_reference",
        "usage": "anchors Ti/Pt ordinary material composition as standard atomic species, not hidden test-body sectors",
        "confidence": "source_anchor_materials_not_alloy_inventory",
        "valid_for_claim": "false",
    },
    {
        "web_source_id": "WEB3349_5_ciaaw_elements",
        "title": "CIAAW Standard Atomic Weights",
        "url": "https://ciaaw.org/atomic-weights.htm",
        "source_type": "measurement_reference",
        "usage": "secondary anchor for ordinary element composition in Ti/Pt material inventories",
        "confidence": "source_anchor_materials_not_alloy_inventory",
        "valid_for_claim": "false",
    },
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3349_LOCAL_SOURCE_REGISTER.csv",
    "web_sources": OUT / "P8_Y5_R2FR_3349_WEB_SOURCE_REGISTER.csv",
    "nodes": OUT / "P8_Y5_R2FR_3349_GRAPH_NODE_BASIS_SOURCE_SIGN.csv",
    "edges": OUT / "P8_Y5_R2FR_3349_GRAPH_EDGE_CERTIFICATE.csv",
    "closure": OUT / "P8_Y5_R2FR_3349_GRAPH_CLOSURE_THEOREM_STATUS.csv",
    "rab": OUT / "P8_Y5_R2FR_3349_RAB_ZERO_PROMOTION_GATE.csv",
    "fallback": OUT / "P8_Y5_R2FR_3349_FALLBACK_MATERIAL_TABLE_TRIGGER.csv",
    "decision": OUT / "P8_Y5_R2FR_3349_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3349_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3349_VALIDATION.csv",
}


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        if path.suffix.lower() == ".csv":
            read_csv(path)
        else:
            path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def local_source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, role in LOCAL_SOURCES:
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def web_source_rows() -> list[dict[str, Any]]:
    return WEB_SOURCES


def node_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "node_id": "NODE3349_0_charged_leptons",
            "ordinary_component": "electrons / charged leptonic matter",
            "graph_role": "charged matter node coupled to EM/gauge sector",
            "source_anchor_ids": "WEB3349_2_pdg_standard_model; WEB3349_1_em_stress_exchange",
            "source_signed": "true",
            "promotion_status": "SOURCE_ANCHORED_NODE",
            "remaining_gap": "material/alloy inventory and parent source-map ownership still not closed",
            "valid_for_claim": "false",
        },
        {
            "node_id": "NODE3349_1_baryons_quarks",
            "ordinary_component": "protons/neutrons as baryonic/quark-gluon matter",
            "graph_role": "nuclear matter node coupled through QCD/nuclear binding",
            "source_anchor_ids": "WEB3349_2_pdg_standard_model; WEB3349_3_pdg_qcd",
            "source_signed": "true",
            "promotion_status": "SOURCE_ANCHORED_NODE",
            "remaining_gap": "no material-specific nuclear binding decomposition yet",
            "valid_for_claim": "false",
        },
        {
            "node_id": "NODE3349_2_em_binding",
            "ordinary_component": "EM field and EM binding stress",
            "graph_role": "exchange edge carrier between charged constituents",
            "source_anchor_ids": "WEB3349_1_em_stress_exchange",
            "source_signed": "true",
            "promotion_status": "SOURCE_ANCHORED_BINDING_NODE",
            "remaining_gap": "falloff/boundary/improvement convention not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "node_id": "NODE3349_3_nuclear_binding",
            "ordinary_component": "strong/nuclear binding stress",
            "graph_role": "exchange edge carrier inside nuclei",
            "source_anchor_ids": "WEB3349_3_pdg_qcd",
            "source_signed": "true",
            "promotion_status": "SOURCE_ANCHORED_BINDING_NODE",
            "remaining_gap": "nuclear effective model and binding-energy convention not source-table closed",
            "valid_for_claim": "false",
        },
        {
            "node_id": "NODE3349_4_TiPt_materials",
            "ordinary_component": "Titanium / Platinum test-body ordinary atomic material",
            "graph_role": "MICROSCOPE material arena anchor",
            "source_anchor_ids": "WEB3349_4_nist_atomic_weights; WEB3349_5_ciaaw_elements",
            "source_signed": "true",
            "promotion_status": "ELEMENT_ANCHORED_NOT_ALLOY_CLOSED",
            "remaining_gap": "exact MICROSCOPE alloy composition and binding-energy inventory not acquired",
            "valid_for_claim": "false",
        },
    ]


def edge_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "edge_id": "EDGE3349_0_electron_EM_nucleus",
            "edge": "charged lepton -- EM/binding stress -- nucleus",
            "exchange_constraint": "C_e^nu + C_EM/bind^nu + C_nucleus^nu = 0 for the interacting ordinary subsystem",
            "source_anchor_ids": "WEB3349_1_em_stress_exchange; WEB3349_2_pdg_standard_model",
            "source_signed": "true",
            "certificate_status": "SOURCE_ANCHORED_STANDARD_EDGE",
            "promotion_gap": "not yet a material-specific Hilbert-stress decomposition for Ti/Pt alloys",
            "valid_for_claim": "false",
        },
        {
            "edge_id": "EDGE3349_1_proton_neutron_nuclear_binding",
            "edge": "proton/quark matter -- strong/nuclear binding -- neutron/quark matter",
            "exchange_constraint": "C_p^nu + C_n^nu + C_nuclear_bind^nu = 0 in the effective nuclear subsystem",
            "source_anchor_ids": "WEB3349_3_pdg_qcd",
            "source_signed": "true",
            "certificate_status": "SOURCE_ANCHORED_STANDARD_EDGE",
            "promotion_gap": "effective nuclear component convention and binding stress split not closed",
            "valid_for_claim": "false",
        },
        {
            "edge_id": "EDGE3349_2_atom_molecule_lattice_inheritance",
            "edge": "atoms/molecules/solids inherit a total ordinary Hilbert source from constituent plus binding stresses",
            "exchange_constraint": "T_body = T_rest + T_EM_bind + T_nuclear_bind + T_lattice + ...",
            "source_anchor_ids": "WEB3349_1_em_stress_exchange; WEB3349_3_pdg_qcd; WEB3349_4_nist_atomic_weights",
            "source_signed": "true",
            "certificate_status": "SOURCE_ANCHORED_MACROSCOPIC_INHERITANCE",
            "promotion_gap": "lattice/material model and alloy inventory not closed",
            "valid_for_claim": "false",
        },
        {
            "edge_id": "EDGE3349_3_decoupled_hidden_block_exclusion",
            "edge": "ordinary test body -- no exchange -- hidden/decoupled block",
            "exchange_constraint": "T_D excluded from ordinary Ti/Pt body unless source inventory explicitly includes it",
            "source_anchor_ids": "LSRC3349_3_2616_graph_attempt; LSRC3349_4_2616_connectivity",
            "source_signed": "false",
            "certificate_status": "ARENA_EXCLUSION_NOT_SOURCE_SIGNED",
            "promotion_gap": "requires explicit local arena inventory excluding dark/hidden/decoupled source blocks from the tested bodies",
            "valid_for_claim": "false",
        },
    ]


def closure_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "closure_id": "CLOSE3349_0_graph_edges",
            "claim_piece": "ordinary matter graph has source-backed standard edges",
            "result": "PARTIAL_SOURCE_SIGNED",
            "evidence": "EM, QCD/strong, Standard Model, and Ti/Pt element anchors are recorded",
            "missing_for_promotion": "material-specific alloy inventory, binding-energy convention, and decoupled-block arena exclusion",
            "valid_for_claim": "false",
        },
        {
            "closure_id": "CLOSE3349_1_connected_component_weight",
            "claim_piece": "connected graph collapses relative source weights to one common measured-G mode",
            "result": "THEOREM_AVAILABLE_IF_GRAPH_AND_PARENT_SIGNED",
            "evidence": "3348 theorem and 3345/2616 collapse rows",
            "missing_for_promotion": "parent source-map ownership and graph closure both required",
            "valid_for_claim": "false",
        },
        {
            "closure_id": "CLOSE3349_2_decoupled_exception",
            "claim_piece": "no decoupled block contributes to local ordinary Ti/Pt test bodies",
            "result": "NOT_CLOSED",
            "evidence": "local corpus has an arena-exclusion contract but not a source-backed local inventory",
            "missing_for_promotion": "test-body source inventory excluding hidden/dark/decoupled conserved blocks",
            "valid_for_claim": "false",
        },
        {
            "closure_id": "CLOSE3349_3_RAB_zero_route",
            "claim_piece": "R_AB=0 no-independent-slot route",
            "result": "NOT_PROMOTED",
            "evidence": "source anchors strengthen the graph route but do not close every promotion clause",
            "missing_for_promotion": "CLOSE3349_1 plus CLOSE3349_2 plus parent source-map no-projector signature",
            "valid_for_claim": "false",
        },
    ]


def rab_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3349_0_source_anchors_recorded",
            "claim": "ordinary matter graph has external source anchors",
            "passed": "true",
            "reason": "web source register includes Hilbert/EM/SM/QCD/NIST/CIAAW anchors and graph rows link to them",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3349_1_graph_closed_for_TiPt",
            "claim": "Ti/Pt ordinary matter graph is fully closed",
            "passed": "false",
            "reason": "exact alloy/material inventory and binding-energy decomposition remain absent",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3349_2_decoupled_arena_excluded",
            "claim": "decoupled nonordinary source blocks are excluded from the local WEP arena",
            "passed": "false",
            "reason": "arena exclusion is a contract but not source-signed for the tested bodies",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3349_3_RAB_zero_promoted",
            "claim": "R_AB=0 is promoted for current MTS local ordinary matter",
            "passed": "false",
            "reason": "source anchors are not enough without graph closure, decoupled exclusion, and parent no-projector signature",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3349_4_local_GR_claim",
            "claim": "local GR/Newton source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "R_AB zero route improved but not promoted; finite material-charge fallback remains open",
            "valid_for_claim": "false",
        },
    ]


def fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "fallback_id": "FB3349_0_material_table_needed_if_graph_not_closed",
            "trigger": "GATE3349_1_graph_closed_for_TiPt=false or GATE3349_2_decoupled_arena_excluded=false",
            "fallback_action": "build Ti/Pt material charge table with electron/proton/neutron, EM binding, nuclear binding, alloy composition, and beta-normalization rows",
            "relationship_to_RAB": "R_TiPt=beta dot Delta chi_TiPt on the explicit spurion branch",
            "claim_status": "nonclaim_until_source_backed_and_parent_owned",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "FB3349_1_graph_route_still_preferred",
            "trigger": "ordinary graph evidence improves but does not close",
            "fallback_action": "first try arena inventory/exclusion before fitting material charges",
            "relationship_to_RAB": "if graph closes, no independent ordinary R_AB slot remains",
            "claim_status": "preferred_derivation_route",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3349_0",
            "question": "Did 3349 source-sign the ordinary matter graph enough to promote R_AB=0?",
            "answer": "not yet",
            "reason": "standard EM/QCD/SM/material anchors are now recorded, but Ti/Pt alloy inventory, binding split, decoupled arena exclusion, and parent no-projector signature remain open",
            "next_action": "close the local arena inventory/exclusion before falling back to charge fitting",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3349_1",
            "question": "Did 3349 move the work forward?",
            "answer": "yes",
            "reason": "the graph route is now source-anchored rather than private-only, and its exact promotion blockers are separated from the finite material-table fallback",
            "next_action": "3350 should build a local ordinary source-arena inventory for MICROSCOPE-like bodies",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3350-Y5-R2FR-local-ordinary-source-arena-inventory-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3350_local_ordinary_source_arena_inventory.py",
            "objective": "build the local source-arena inventory that either excludes decoupled/hidden blocks from ordinary Ti/Pt-like test bodies or forces them into explicit finite residual rows",
            "why_next": "this is the remaining graph-route blocker before falling back to arbitrary material-charge response fitting",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3349b-Y5-R2FR-TiPt-material-charge-table-nonclaim.md",
            "target_script": "scripts/Y5_R2FR_3349b_TiPt_material_charge_table_nonclaim.py",
            "objective": "fallback branch: acquire Ti/Pt composition and build nonclaim Delta chi rows for beta dot Delta chi_TiPt",
            "why_next": "needed if 3350 cannot close the no-independent-slot graph route",
            "valid_for_claim": "false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]], limit: int = 20) -> str:
    if not rows:
        return "_No rows._"
    fieldnames: list[str] = []
    for row in rows[:limit]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows[:limit]:
        values = [compact(row.get(key, ""), 260).replace("|", "\\|") for key in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def render_doc() -> str:
    return "\n\n".join(
        [
            "# 3349 — Source-Backed Ordinary Matter Graph Certificate Under AX1090",
            f"Generated: `{RUN_UTC}`",
            "## Summary\n"
            "- This checkpoint attacks the 3348 graph route: source-sign ordinary matter connectivity before falling back to material charge fitting.\n"
            "- Progress: the electron/EM/nuclear/macroscopic material graph is no longer private-only; it now has external source anchors.\n"
            "- Verdict: `R_AB=0` is still not promoted, because graph closure needs Ti/Pt arena inventory, binding conventions, decoupled-block exclusion, and the parent no-projector signature.\n"
            "- This is still useful: the remaining blockers are now separated from the fallback `R_TiPt=beta dot Delta chi_TiPt` charge-table branch.",
            "## Web Source Register\n" + markdown_table(web_source_rows()),
            "## Graph Node Basis Source Sign\n" + markdown_table(node_basis_rows()),
            "## Graph Edge Certificate\n" + markdown_table(edge_certificate_rows()),
            "## Graph Closure Theorem Status\n" + markdown_table(closure_status_rows()),
            "## RAB Zero Promotion Gate\n" + markdown_table(rab_gate_rows()),
            "## Fallback Material Table Trigger\n" + markdown_table(fallback_rows()),
            "## Decision Ledger\n" + markdown_table(decision_rows()),
            "## Next Target\n" + markdown_table(next_target_rows()),
        ]
    ) + "\n"


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    local_sources = local_source_rows()
    web_sources = web_source_rows()
    nodes = node_basis_rows()
    edges = edge_certificate_rows()
    closures = closure_status_rows()
    gates = rab_gate_rows()
    formalization_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3349_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3349_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3349_2_web_sources_well_formed",
            "check": "all web source URLs are nonempty http links",
            "passed": all(row["url"].startswith("http") for row in web_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3349_3_outputs_parse",
            "check": "all 3349 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3349_4_nodes_source_anchored",
            "check": "graph node basis has source anchors and no MISSING markers",
            "passed": all(row["source_signed"] == "true" and "MISSING_" not in "|".join(row.values()) for row in nodes),
            "detail": "",
        },
        {
            "check_id": "VAL3349_5_edges_include_required_families",
            "check": "edge certificate includes EM, nuclear, macroscopic inheritance, and decoupled exception rows",
            "passed": {row["edge_id"] for row in edges}
            == {"EDGE3349_0_electron_EM_nucleus", "EDGE3349_1_proton_neutron_nuclear_binding", "EDGE3349_2_atom_molecule_lattice_inheritance", "EDGE3349_3_decoupled_hidden_block_exclusion"},
            "detail": "",
        },
        {
            "check_id": "VAL3349_6_closure_not_overclaimed",
            "check": "closure rows do not promote R_AB zero",
            "passed": any(row["closure_id"] == "CLOSE3349_3_RAB_zero_route" and row["result"] == "NOT_PROMOTED" for row in closures),
            "detail": "",
        },
        {
            "check_id": "VAL3349_7_RAB_zero_gate_false",
            "check": "R_AB zero and local-GR claim gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3349_3_RAB_zero_promoted", "GATE3349_4_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3349_8_fallback_triggered",
            "check": "fallback table trigger is recorded but nonclaim",
            "passed": all(row["valid_for_claim"] == "false" for row in fallback_rows()) and any("Delta chi" in row["relationship_to_RAB"] for row in fallback_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3349_9_next_target_arena_inventory",
            "check": "next target prioritizes local source-arena inventory before charge fitting",
            "passed": any("source-arena inventory" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3349_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3349_11_overall",
            "check": "3349 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["local_sources"], local_source_rows())
    write_csv(OUTPUTS["web_sources"], web_source_rows())
    write_csv(OUTPUTS["nodes"], node_basis_rows())
    write_csv(OUTPUTS["edges"], edge_certificate_rows())
    write_csv(OUTPUTS["closure"], closure_status_rows())
    write_csv(OUTPUTS["rab"], rab_gate_rows())
    write_csv(OUTPUTS["fallback"], fallback_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
