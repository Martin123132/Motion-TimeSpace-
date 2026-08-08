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
DOC = ROOT / "3350-Y5-R2FR-local-ordinary-source-arena-inventory-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3350_0_3349_doc", ROOT / "3349-Y5-R2FR-source-backed-ordinary-matter-graph-certificate-under-AX1090.md", "3349 graph certificate handoff"),
    ("LSRC3350_1_3349_edges", OUT / "P8_Y5_R2FR_3349_GRAPH_EDGE_CERTIFICATE.csv", "3349 graph edge certificate"),
    ("LSRC3350_2_3349_closure", OUT / "P8_Y5_R2FR_3349_GRAPH_CLOSURE_THEOREM_STATUS.csv", "3349 graph closure status"),
    ("LSRC3350_3_3349_gates", OUT / "P8_Y5_R2FR_3349_RAB_ZERO_PROMOTION_GATE.csv", "3349 RAB gate status"),
    ("LSRC3350_4_3349_web", OUT / "P8_Y5_R2FR_3349_WEB_SOURCE_REGISTER.csv", "3349 web source anchors"),
    ("LSRC3350_5_3348_basis", OUT / "P8_Y5_R2FR_3348_MATERIAL_RESPONSE_BASIS.csv", "3348 response-basis fork"),
    ("LSRC3350_6_3342_wep", OUT / "P8_Y5_R2FR_3342_WEP_BOUND_ROWS.csv", "3342 MICROSCOPE WEP bound rows"),
    ("LSRC3350_7_3342_material", OUT / "P8_Y5_R2FR_3342_MATERIAL_RESPONSE_PLACEHOLDERS.csv", "3342 material response placeholder guard"),
]

WEB_SOURCES = [
    {
        "web_source_id": "WEB3350_0_MICROSCOPE_TiPt",
        "title": "MICROSCOPE Mission final Ti/Pt equivalence-principle result",
        "url": "https://link.aps.org/doi/10.1103/PhysRevLett.129.121102",
        "usage": "anchors the local WEP arena as ordinary Ti/Pt test masses with measured eta_TiPt",
        "scope": "ordinary material test-body arena, not a parent MTS source signature",
        "valid_for_claim": "false",
    },
    {
        "web_source_id": "WEB3350_1_NIST_atomic_compositions",
        "title": "NIST Atomic Weights and Isotopic Compositions",
        "url": "https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl",
        "usage": "anchors Ti/Pt as standard ordinary atomic elements",
        "scope": "element-level material identity, not exact MICROSCOPE alloy decomposition",
        "valid_for_claim": "false",
    },
    {
        "web_source_id": "WEB3350_2_PDG_standard_model",
        "title": "Particle Data Group Review: The Standard Model",
        "url": "https://pdg.lbl.gov/2023/reviews/rpp2023-rev-standard-model.pdf",
        "usage": "anchors ordinary matter/gauge sectors in the source-arena inventory",
        "scope": "ordinary-sector component classification",
        "valid_for_claim": "false",
    },
    {
        "web_source_id": "WEB3350_3_PDG_QCD",
        "title": "Particle Data Group Review: Quantum Chromodynamics",
        "url": "https://pdg.lbl.gov/2023/reviews/rpp2023-rev-qcd.pdf",
        "usage": "anchors nuclear/strong binding as ordinary-sector content",
        "scope": "ordinary-sector binding classification, not material-specific binding table",
        "valid_for_claim": "false",
    },
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3350_LOCAL_SOURCE_REGISTER.csv",
    "web_sources": OUT / "P8_Y5_R2FR_3350_WEB_SOURCE_REGISTER.csv",
    "arena": OUT / "P8_Y5_R2FR_3350_LOCAL_ARENA_DEFINITION.csv",
    "ordinary": OUT / "P8_Y5_R2FR_3350_ORDINARY_SOURCE_INVENTORY.csv",
    "decoupled": OUT / "P8_Y5_R2FR_3350_DECOUPLED_BLOCK_AUDIT.csv",
    "theorem": OUT / "P8_Y5_R2FR_3350_ARENA_EXCLUSION_THEOREM.csv",
    "residuals": OUT / "P8_Y5_R2FR_3350_EXPLICIT_RESIDUAL_ROWS.csv",
    "rab": OUT / "P8_Y5_R2FR_3350_RAB_ZERO_ROUTE_UPDATE.csv",
    "decision": OUT / "P8_Y5_R2FR_3350_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3350_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3350_VALIDATION.csv",
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


def arena_definition_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "ARENA3350_0_MICROSCOPE_TiPt_material",
            "arena": "local WEP Ti/Pt ordinary material test-body arena",
            "included_source_domain": "ordinary atomic/electronic/nuclear/material Hilbert stress of Ti/Pt-like test bodies",
            "excluded_by_definition": "nonordinary hidden/dark/decoupled blocks not listed as test-body material constituents",
            "not_excluded_by_definition": "ambient/background parent fields, hidden sectors coupled through the field equation, readout/projector terms",
            "source_anchor_ids": "WEB3350_0_MICROSCOPE_TiPt; WEB3350_1_NIST_atomic_compositions",
            "status": "ARENA_SPLIT_DEFINED",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3350_1_parent_field_equation",
            "arena": "local parent field-equation source arena",
            "included_source_domain": "all variational source terms admitted by S_parent plus explicit residual blocks",
            "excluded_by_definition": "nothing beyond the signed parent action object language",
            "not_excluded_by_definition": "decoupled conserved sectors if present in S_parent or local environment",
            "source_anchor_ids": "LSRC3350_0_3349_doc; LSRC3350_5_3348_basis",
            "status": "FIELD_EQUATION_ARENA_REMAINS_PARENT_SIGNED_ONLY",
            "valid_for_claim": "false",
        },
    ]


def ordinary_source_inventory_rows() -> list[dict[str, Any]]:
    return [
        {
            "inventory_id": "ORD3350_0_electrons",
            "ordinary_component": "bound electrons / charged leptonic matter",
            "arena_status": "included_in_ordinary_TiPt_material",
            "graph_connection": "connected to nuclei through EM/binding stress",
            "source_anchor_ids": "WEB3350_2_PDG_standard_model; LSRC3350_1_3349_edges",
            "RAB_role": "part of total Hilbert stress; no independent R_AB if graph closes",
            "valid_for_claim": "false",
        },
        {
            "inventory_id": "ORD3350_1_nuclear_matter",
            "ordinary_component": "protons/neutrons/quark-gluon nuclear content",
            "arena_status": "included_in_ordinary_TiPt_material",
            "graph_connection": "connected through strong/nuclear binding",
            "source_anchor_ids": "WEB3350_2_PDG_standard_model; WEB3350_3_PDG_QCD",
            "RAB_role": "part of total Hilbert stress; no independent R_AB if graph closes",
            "valid_for_claim": "false",
        },
        {
            "inventory_id": "ORD3350_2_binding_stresses",
            "ordinary_component": "EM, nuclear, molecular, and lattice binding stresses",
            "arena_status": "included_in_ordinary_TiPt_material_as_binding_content",
            "graph_connection": "edge carriers that make the ordinary material graph connected",
            "source_anchor_ids": "LSRC3350_1_3349_edges",
            "RAB_role": "must be included in T_H rather than counted as a separate source projector",
            "valid_for_claim": "false",
        },
        {
            "inventory_id": "ORD3350_3_alloy_material_detail",
            "ordinary_component": "exact MICROSCOPE Ti/Pt alloy and material processing detail",
            "arena_status": "not_acquired",
            "graph_connection": "needed only for material-charge fallback or fine source table",
            "source_anchor_ids": "WEB3350_0_MICROSCOPE_TiPt; WEB3350_1_NIST_atomic_compositions",
            "RAB_role": "not needed for pure Hilbert zero theorem, but needed for nonzero beta dot Delta chi_TiPt fallback",
            "valid_for_claim": "false",
        },
    ]


def decoupled_block_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "block_id": "DECPL3350_0_material_constituent_hidden_block",
            "candidate_block": "hidden/dark/decoupled sector as literal Ti/Pt material constituent",
            "arena_result": "EXCLUDED_FROM_ORDINARY_MATERIAL_INVENTORY",
            "reason": "Ti/Pt material arena is defined by ordinary atomic/nuclear constituents and binding stresses; no source anchor lists a hidden-sector constituent",
            "remaining_risk": "does not exclude a parent hidden field coupled to local gravity outside material composition",
            "residual_symbol": "none_for_material_inventory; epsilon_decoupled_field remains",
            "valid_for_claim": "false",
        },
        {
            "block_id": "DECPL3350_1_ambient_decoupled_background",
            "candidate_block": "ambient/background decoupled conserved source block",
            "arena_result": "NOT_EXCLUDED_FROM_PARENT_FIELD_ARENA",
            "reason": "ordinary material composition does not prove the local parent field equation lacks a separately conserved residual block",
            "remaining_risk": "could enter common source calibration, PPN, WEP, or local field equation as an explicit residual",
            "residual_symbol": "epsilon_decoupled_field",
            "valid_for_claim": "false",
        },
        {
            "block_id": "DECPL3350_2_readout_projector_shadow",
            "candidate_block": "readout/projector-created apparent decoupled source",
            "arena_result": "NOT_EXCLUDED_UNTIL_PARENT_NO_PROJECTOR_SIGNED",
            "reason": "3350 inventories material sources, not the whole readout grammar",
            "remaining_risk": "source-shadow/readout residual can imitate a material response",
            "residual_symbol": "epsilon_readout_source_shadow",
            "valid_for_claim": "false",
        },
        {
            "block_id": "DECPL3350_3_boundary_improvement_contact",
            "candidate_block": "boundary/improvement/contact source near test bodies",
            "arena_result": "NOT_EXCLUDED_UNTIL_BOUNDARY_CONDITION_SIGNED",
            "reason": "binding stresses belong in T_H, but unclassified boundary/contact terms are a separate parent-action issue",
            "remaining_risk": "finite local contact residual if boundary conditions fail",
            "residual_symbol": "epsilon_boundary_contact",
            "valid_for_claim": "false",
        },
    ]


def arena_exclusion_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "AEX3350_0_material_exclusion",
            "claim_piece": "hidden/decoupled blocks are not ordinary Ti/Pt material constituents",
            "mathematical_form": "T_material^TiPt = T_e + T_nuc + T_EM_bind + T_nuclear_bind + T_lattice + ... ; T_D not in T_material unless the material inventory explicitly includes it",
            "result": "CONDITIONAL_MATERIAL_ARENA_EXCLUSION",
            "promotion_limit": "does not exclude T_D from S_parent or from ambient/local field-equation sources",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "AEX3350_1_graph_route_update",
            "claim_piece": "ordinary material branch of R_AB has no hidden constituent slot",
            "mathematical_form": "R_AB^ordinary=0 if T_active=T_H and ordinary graph is connected; hidden T_D is not a material-composition correction but a separate residual branch",
            "result": "GRAPH_ROUTE_STRENGTHENED_NOT_PROMOTED",
            "promotion_limit": "parent no-projector/source-shadow signature and field-equation decoupled-block bound remain open",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "AEX3350_2_no_smuggling_rule",
            "claim_piece": "do not hide decoupled blocks inside R_AB",
            "mathematical_form": "R_TiPt=beta dot Delta chi_TiPt only for explicit material/source charges; T_D uses epsilon_decoupled_field or epsilon_boundary_contact rows",
            "result": "CLASSIFICATION_RULE_DERIVED",
            "promotion_limit": "finite residual rows still need numeric/source-backed couplings or parent zeros",
            "valid_for_claim": "false",
        },
    ]


def explicit_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RES3350_0_epsilon_decoupled_field",
            "symbol": "epsilon_decoupled_field",
            "meaning": "separately conserved nonordinary/hidden/background source contribution to the local parent field equation",
            "arena": "parent field-equation source arena",
            "bound_form": "||T_D|| / ||T_H^ordinary|| times coupling/projection factor",
            "numeric_status": "MISSING_DENSITY_COUPLING_AND_PARENT_OWNERSHIP",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3350_1_epsilon_readout_source_shadow",
            "symbol": "epsilon_readout_source_shadow",
            "meaning": "apparent source block created by post-solution readout/projector operation",
            "arena": "readout/source-shadow grammar",
            "bound_form": "projector norm times source-shadow amplitude",
            "numeric_status": "MISSING_PARENT_NO_PROJECTOR_SIGNATURE_OR_NUMERIC_PROJECTOR_NORM",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3350_2_epsilon_boundary_contact",
            "symbol": "epsilon_boundary_contact",
            "meaning": "boundary/improvement/contact source term not included in ordinary bulk Hilbert material stress",
            "arena": "boundary/contact local source arena",
            "bound_form": "boundary flux/contact term divided by ordinary bulk Hilbert source norm",
            "numeric_status": "MISSING_BOUNDARY_CONDITION_OR_CONTACT_BOUND",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def rab_route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3350_0_material_arena_split",
            "claim": "ordinary Ti/Pt material arena is separated from parent field-equation arena",
            "passed": "true",
            "reason": "3350 explicitly distinguishes ordinary material constituents from ambient/parent residual sources",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3350_1_hidden_material_constituent_excluded",
            "claim": "hidden/decoupled blocks are excluded from ordinary Ti/Pt material inventory unless explicitly listed",
            "passed": "true",
            "reason": "ordinary material inventory uses atomic/nuclear/binding components; hidden blocks are moved to residual rows",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3350_2_parent_decoupled_field_excluded",
            "claim": "decoupled/hidden blocks are excluded from the local parent field-equation arena",
            "passed": "false",
            "reason": "material composition does not prove parent field equation has no T_D or boundary/source-shadow residual",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3350_3_RAB_zero_promoted",
            "claim": "R_AB=0 no-independent-slot route is promoted",
            "passed": "false",
            "reason": "ordinary material branch is cleaner, but parent no-projector and decoupled field residuals remain open",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3350_4_local_GR_claim",
            "claim": "local GR/Newton source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "explicit residual rows remain without parent zeros or numeric bounds",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3350_0",
            "question": "Did 3350 close the decoupled-block blocker?",
            "answer": "partly",
            "reason": "hidden/decoupled blocks are excluded from ordinary Ti/Pt material composition, but not from the full parent field equation",
            "next_action": "try to prove parent no-decoupled-field/no-boundary-contact for local ordinary arenas, or source finite residual bounds",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3350_1",
            "question": "Did 3350 reduce the need for charge fitting?",
            "answer": "yes",
            "reason": "ordinary material R_AB stays on the Hilbert-zero branch; charge fitting is only for explicit spurion/projector branches, not hidden blocks smuggled into material response",
            "next_action": "3351 should attack parent decoupled-field silence before 3349b charge-table fallback",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3351-Y5-R2FR-parent-decoupled-field-silence-or-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3351_parent_decoupled_field_silence_or_bound.py",
            "objective": "prove local parent action has no separately conserved decoupled source block in ordinary WEP/PPN arenas, or convert epsilon_decoupled_field into sourced finite residual rows",
            "why_next": "3350 moved hidden blocks out of material R_AB, but the parent field-equation arena still needs a zero or bound",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3349b-Y5-R2FR-TiPt-material-charge-table-nonclaim.md",
            "target_script": "scripts/Y5_R2FR_3349b_TiPt_material_charge_table_nonclaim.py",
            "objective": "fallback branch for explicit spurion/projector material charges beta dot Delta chi_TiPt",
            "why_next": "needed only if a nonzero source-projector charge basis is deliberately retained",
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
            "# 3350 — Local Ordinary Source-Arena Inventory Under AX1090",
            f"Generated: `{RUN_UTC}`",
            "## Summary\n"
            "- This checkpoint attacks the decoupled-block blocker left by 3349.\n"
            "- Result: hidden/decoupled blocks are excluded from the ordinary Ti/Pt material inventory unless explicitly listed, but they are not thereby excluded from the full parent field-equation arena.\n"
            "- So `R_AB=0` is strengthened for the ordinary material graph, while `epsilon_decoupled_field`, `epsilon_readout_source_shadow`, and `epsilon_boundary_contact` remain explicit nonclaim residual rows.\n"
            "- This prevents smuggling hidden blocks into a fake material response factor and keeps the local-GR route honest.",
            "## Web Source Register\n" + markdown_table(web_source_rows()),
            "## Local Arena Definition\n" + markdown_table(arena_definition_rows()),
            "## Ordinary Source Inventory\n" + markdown_table(ordinary_source_inventory_rows()),
            "## Decoupled Block Audit\n" + markdown_table(decoupled_block_audit_rows()),
            "## Arena Exclusion Theorem\n" + markdown_table(arena_exclusion_theorem_rows()),
            "## Explicit Residual Rows\n" + markdown_table(explicit_residual_rows()),
            "## RAB Zero Route Update\n" + markdown_table(rab_route_update_rows()),
            "## Decision Ledger\n" + markdown_table(decision_rows()),
            "## Next Target\n" + markdown_table(next_target_rows()),
        ]
    ) + "\n"


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    local_sources = local_source_rows()
    arenas = arena_definition_rows()
    ordinary = ordinary_source_inventory_rows()
    decoupled = decoupled_block_audit_rows()
    residuals = explicit_residual_rows()
    gates = rab_route_update_rows()
    formalization_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3350_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3350_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3350_2_web_sources_well_formed",
            "check": "all web source URLs are nonempty http links",
            "passed": all(row["url"].startswith("http") for row in web_source_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3350_3_outputs_parse",
            "check": "all 3350 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3350_4_arena_split_present",
            "check": "arena definition separates material inventory from parent field-equation arena",
            "passed": {row["arena_id"] for row in arenas} == {"ARENA3350_0_MICROSCOPE_TiPt_material", "ARENA3350_1_parent_field_equation"},
            "detail": "",
        },
        {
            "check_id": "VAL3350_5_ordinary_inventory_complete",
            "check": "ordinary inventory includes electrons, nuclear matter, binding stresses, and alloy-detail row",
            "passed": {row["inventory_id"] for row in ordinary}
            == {"ORD3350_0_electrons", "ORD3350_1_nuclear_matter", "ORD3350_2_binding_stresses", "ORD3350_3_alloy_material_detail"},
            "detail": "",
        },
        {
            "check_id": "VAL3350_6_decoupled_split_correct",
            "check": "decoupled audit excludes material constituent block but keeps parent field block open",
            "passed": any(row["block_id"] == "DECPL3350_0_material_constituent_hidden_block" and row["arena_result"] == "EXCLUDED_FROM_ORDINARY_MATERIAL_INVENTORY" for row in decoupled)
            and any(row["block_id"] == "DECPL3350_1_ambient_decoupled_background" and row["arena_result"] == "NOT_EXCLUDED_FROM_PARENT_FIELD_ARENA" for row in decoupled),
            "detail": "",
        },
        {
            "check_id": "VAL3350_7_explicit_residuals_created",
            "check": "explicit residual rows exist for decoupled field, readout source shadow, and boundary contact",
            "passed": {row["symbol"] for row in residuals} == {"epsilon_decoupled_field", "epsilon_readout_source_shadow", "epsilon_boundary_contact"},
            "detail": "",
        },
        {
            "check_id": "VAL3350_8_no_overclaim",
            "check": "parent decoupled exclusion, R_AB zero, and local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3350_2_parent_decoupled_field_excluded", "GATE3350_3_RAB_zero_promoted", "GATE3350_4_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3350_9_next_target_decoupled_silence",
            "check": "next target attacks parent decoupled-field silence or bound",
            "passed": any("decoupled source block" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3350_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3350_11_overall",
            "check": "3350 validation overall",
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
    write_csv(OUTPUTS["arena"], arena_definition_rows())
    write_csv(OUTPUTS["ordinary"], ordinary_source_inventory_rows())
    write_csv(OUTPUTS["decoupled"], decoupled_block_audit_rows())
    write_csv(OUTPUTS["theorem"], arena_exclusion_theorem_rows())
    write_csv(OUTPUTS["residuals"], explicit_residual_rows())
    write_csv(OUTPUTS["rab"], rab_route_update_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
