from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3356-Y5-R2FR-local-collar-contact-support-exclusion-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3356_0_3355_doc", ROOT / "3355-Y5-R2FR-boundary-contact-zero-flux-or-contact-bound-under-AX1090.md", "3355 boundary/contact split and next target"),
    ("LSRC3356_1_3355_decomposition", OUT / "P8_Y5_R2FR_3355_BOUNDARY_CONTACT_DECOMPOSITION.csv", "contact/interface survivor definition"),
    ("LSRC3356_2_3355_lemmas", OUT / "P8_Y5_R2FR_3355_ZERO_FLUX_LEMMA_ROWS.csv", "compact support and contact survivor lemmas"),
    ("LSRC3356_3_3355_eps", OUT / "P8_Y5_R2FR_3355_EPSILON_BOUNDARY_CONTACT_SPLIT.csv", "epsilon boundary/contact split"),
    ("LSRC3356_4_3355_bounds", OUT / "P8_Y5_R2FR_3355_CONTACT_BOUND_TEMPLATE.csv", "numeric contact-bound template"),
    ("LSRC3356_5_3355_gates", OUT / "P8_Y5_R2FR_3355_PROMOTION_GATES.csv", "3355 gate status"),
    ("LSRC3356_6_3354_alias", OUT / "P8_Y5_R2FR_3354_ALIAS_FAMILY_INVENTORY.csv", "alias closure handoff"),
    ("LSRC3356_7_3350_residuals", OUT / "P8_Y5_R2FR_3350_EXPLICIT_RESIDUAL_ROWS.csv", "original local residual rows"),
    ("LSRC3356_8_boundary_alpha3", OUT / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "prior boundary no-flux attempt"),
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3356_LOCAL_SOURCE_REGISTER.csv",
    "collar_theorem": OUT / "P8_Y5_R2FR_3356_LOCAL_COLLAR_SUPPORT_THEOREM.csv",
    "arena_classes": OUT / "P8_Y5_R2FR_3356_ARENA_CLASSIFICATION.csv",
    "epsilon_update": OUT / "P8_Y5_R2FR_3356_EPSILON_CONTACT_UPDATE.csv",
    "newton_ppn": OUT / "P8_Y5_R2FR_3356_NEWTON_PPN_IMPLICATIONS.csv",
    "gates": OUT / "P8_Y5_R2FR_3356_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3356_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3356_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3356_VALIDATION.csv",
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
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parseable(path: Path) -> bool:
    try:
        if path.suffix.lower() == ".csv":
            read_csv(path)
        else:
            path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(compact(row.get(key, ""), 260).replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines) + "\n"


def local_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_str(path.exists()),
            "parseable": bool_str(path.exists() and parseable(path)),
            "usage": usage,
            "valid_for_claim": "false",
        }
        for source_id, path, usage in LOCAL_SOURCES
    ]


def collar_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "COL3356_0_contact_support_set",
            "object": "C_contact = supp(T_contact)",
            "statement": "Treat contact/interface leakage as a closed support set for a distributional source term.",
            "proof_or_rule": "Distributional contact terms act only on test variations whose support intersects their support.",
            "result": "DEFINITION_FOR_LOCAL_TEST_FUNCTIONS",
            "claim_scope": "local variational calculus",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "COL3356_1_pointwise_collar",
            "object": "p notin C_contact",
            "statement": "For any local bulk point outside contact support, there exists an open collar/ball U_p with compact closure and U_p cap C_contact = empty.",
            "proof_or_rule": "Closed-set separation/topological locality: positive distance to closed support in a sufficiently small coordinate patch.",
            "result": "PASS_LOCAL_POINTWISE_ZERO",
            "claim_scope": "bulk pointwise Euler-Lagrange equation away from contact support",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "COL3356_2_test_variation_zero",
            "object": "delta fields with supp(delta) subset U_p",
            "statement": "The contact variation is zero for all compact-support variations inside U_p.",
            "proof_or_rule": "<T_contact, delta g> = 0 because supp(delta g) cap supp(T_contact) = empty.",
            "result": "EPSILON_CONTACT_LOCAL_BULK_ZERO",
            "claim_scope": "local bulk equations only",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "COL3356_3_integrated_source_warning",
            "object": "whole body, material surface, orbital/PPN source multipoles",
            "statement": "The collar theorem does not remove contact support that lies on the material boundary or contributes to integrated source multipoles.",
            "proof_or_rule": "Whole-body integrals and exterior fields can receive surface/contact distributions even when pointwise bulk equations away from the surface are clean.",
            "result": "GLOBAL_NEWTON_PPN_NOT_CLOSED",
            "claim_scope": "integrated source normalization and exterior solution",
            "valid_for_claim": "false",
        },
    ]


def arena_classification_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "ARENA3356_0_interior_bulk",
            "arena": "ordinary material interior / vacuum bulk point away from contact support",
            "contact_support_relation": "disjoint by collar choice",
            "epsilon_boundary_contact_status": "0_for_local_bulk_equation",
            "what_this_closes": "pointwise contact leakage in local Euler-Lagrange equation",
            "what_remains_open": "parent-domain signature; whole-source integration",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3356_1_material_surface",
            "arena": "ordinary material boundary or interface",
            "contact_support_relation": "may intersect local source support",
            "epsilon_boundary_contact_status": "OPEN_UNLESS_SURFACE_STRESS_IS_ORDINARY_HILBERT_OR_ZERO",
            "what_this_closes": "nothing global",
            "what_remains_open": "surface stress ownership, contact amplitude, no-marker/no-flux premise",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3356_2_exterior_orbital_field",
            "arena": "exterior gravitational field sourced by integrated body",
            "contact_support_relation": "contact support can affect multipole moments through boundary integrals",
            "epsilon_boundary_contact_status": "OPEN_AS_SOURCE_NORMALIZATION_RESIDUAL",
            "what_this_closes": "local vacuum field equations away from contact support",
            "what_remains_open": "GM normalization, PPN multipoles, orbital source support",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3356_3_scalar_monopole_contact",
            "arena": "universal scalar stationary contact/monopole",
            "contact_support_relation": "support may exist but projects only to constant monopole if premises hold",
            "epsilon_boundary_contact_status": "CALIBRATION_ONLY_IF_PARENT_OWNED",
            "what_this_closes": "vector/preferred-frame leakage conditionally",
            "what_remains_open": "parent ownership of scalar homogeneous marker-free premises",
            "valid_for_claim": "false",
        },
    ]


def epsilon_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "ECU3356_0_pointwise_bulk",
            "symbol": "epsilon_boundary_contact[p]",
            "arena": "p notin supp(T_contact)",
            "value_or_bound": "0",
            "authority": "local collar support theorem",
            "component_status": "EXACT_LOCAL_POINTWISE_ZERO",
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
        },
        {
            "update_id": "ECU3356_1_surface_contact",
            "symbol": "epsilon_boundary_contact_surface",
            "arena": "p in supp(T_contact) or local variations intersect interface",
            "value_or_bound": "MISSING_SURFACE_STRESS_OWNER_OR_NUMERIC_CONTACT_BOUND",
            "authority": "3355 contact template retained",
            "component_status": "OPEN",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "update_id": "ECU3356_2_integrated_source",
            "symbol": "epsilon_boundary_contact_integrated",
            "arena": "whole-body Newton/PPN/orbital source",
            "value_or_bound": "MISSING_INTEGRATED_CONTACT_MULTIPOLE_OR_MONOPOLE_CALIBRATION_THEOREM",
            "authority": "collar theorem explicitly insufficient for integrated source",
            "component_status": "OPEN",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def newton_ppn_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NPPN3356_0_local_vacuum",
            "target": "local vacuum/bulk field equation away from contact support",
            "3356_effect": "contact/interface source term is zero pointwise",
            "status": "IMPROVED_CONDITIONAL_ROUTE",
            "why_not_claim": "left-hand EH/Newton operator and parent-domain signature still need collapse",
            "valid_for_claim": "false",
        },
        {
            "row_id": "NPPN3356_1_Newton_source",
            "target": "Newtonian Poisson source and measured GM",
            "3356_effect": "bulk contact is killed away from surfaces, but surface/contact distributions may renormalize integrated mass",
            "status": "NOT_CLOSED",
            "why_not_claim": "requires surface stress ownership or universal monopole calibration theorem",
            "valid_for_claim": "false",
        },
        {
            "row_id": "NPPN3356_2_PPN_multipoles",
            "target": "PPN residual vector and preferred-frame/source multipoles",
            "3356_effect": "pure scalar stationary boundary remains conditionally safe; vector/contact support remains retained",
            "status": "NOT_CLOSED",
            "why_not_claim": "requires no-marker/no-vector/no-normal-flux parent ownership",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3356_0_pointwise_contact_zero",
            "claim": "epsilon_boundary_contact vanishes for local bulk equations away from contact support",
            "passed": "true",
            "reason": "compact collar disjoint from closed contact support makes distributional contact variation zero",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3356_1_surface_contact_zero_or_bound",
            "claim": "surface/interface contact source is zero, ordinary Hilbert-owned, or source-backed bounded",
            "passed": "false",
            "reason": "surface stress/contact amplitude not parent-owned or numeric",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3356_2_integrated_Newton_source_closed",
            "claim": "integrated Newton/PPN source normalization is closed against contact support",
            "passed": "false",
            "reason": "whole-body surface/contact multipoles remain open",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3356_3_parent_domain_ready_for_collapse",
            "claim": "boundary/contact blocker is reduced enough to attempt parent-domain signature collapse",
            "passed": "true",
            "reason": "remaining contact branch is typed as surface/integrated-source ownership rather than generic boundary leakage",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3356_4_local_GR_claim",
            "claim": "local GR/Newton source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "surface/integrated contact source and parent-domain signature remain unpromoted",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3356_0",
            "question": "Did 3356 prove the contact branch away?",
            "answer": "partly: exact pointwise bulk zero, not whole-source zero",
            "reason": "local collars kill distributional contact terms away from their support, but material surfaces/integrated source multipoles can still matter",
            "next_action": "collapse parent-domain signature with explicit remaining surface/integrated-source caveat, then attack surface stress ownership",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3356_1",
            "question": "Is this enough to try the parent-domain signature certificate?",
            "answer": "yes as an intermediate theorem gate",
            "reason": "generic source-shadow/readout/boundary fog has been reduced to named residuals with exact local-bulk zeros and explicit surface exceptions",
            "next_action": "3357 parent-domain signature collapse attempt",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3357-Y5-R2FR-parent-domain-signature-collapse-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3357_parent_domain_signature_collapse.py",
            "objective": "combine 3346 parent action syntax, 3354 alias reductions, 3355 boundary split, and 3356 collar theorem into one parent-domain signature certificate with explicit remaining surface/integrated-source caveats",
            "why_next": "3356 has narrowed the contact blocker enough that the parent-domain proof can be attempted honestly",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3358-Y5-R2FR-surface-stress-owner-or-contact-multipole-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3358_surface_stress_owner_or_contact_multipole_bound.py",
            "objective": "prove surface/contact stress is ordinary Hilbert-owned or universal monopole-only, or build a finite no-cancellation contact multipole bound",
            "why_next": "this is the remaining Newton/PPN source-normalization survivor after local collar exclusion",
            "valid_for_claim": "false",
        },
    ]


def render_doc() -> str:
    return "\n".join(
        [
            "# 3356 — Local Collar Contact-Support Exclusion Under AX1090",
            "",
            f"Generated: `{RUN_UTC}`",
            "",
            "## Summary",
            "- This checkpoint proves the useful part of the contact route: contact/interface terms vanish for pointwise local bulk equations away from their support.",
            "- The proof is not a handwave: choose a compact collar/ball around a bulk point disjoint from the closed contact support; distributional contact terms then evaluate to zero on all local test variations.",
            "- It does **not** close whole-body Newton/PPN source normalization, because material surfaces or contact multipoles can still affect integrated mass and exterior fields.",
            "- So the local-GR branch improves, but no full local-GR/Newton claim is promoted.",
            "",
            "## Local Source Register",
            table(local_source_rows()),
            "## Local Collar Support Theorem",
            table(collar_theorem_rows()),
            "## Arena Classification",
            table(arena_classification_rows()),
            "## Epsilon Contact Update",
            table(epsilon_update_rows()),
            "## Newton / PPN Implications",
            table(newton_ppn_rows()),
            "## Promotion Gates",
            table(promotion_gate_rows()),
            "## Decision Ledger",
            table(decision_rows()),
            "## Next Target",
            table(next_target_rows()),
        ]
    )


def validate_outputs() -> list[dict[str, Any]]:
    local_sources = local_source_rows()
    theorem = collar_theorem_rows()
    arenas = arena_classification_rows()
    eps = epsilon_update_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    write_targets_outside_fw = all(not path.resolve().is_relative_to(FW.resolve()) for path in output_paths + [DOC])
    checks: list[dict[str, Any]] = [
        {
            "check_id": "VAL3356_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3356_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parseable"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3356_2_outputs_parse",
            "check": "all 3356 non-validation outputs parse",
            "passed": all(path.exists() and parseable(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3356_3_collar_theorem_present",
            "check": "collar theorem includes support set, pointwise collar, test-variation zero, and integrated-source warning",
            "passed": {row["theorem_id"] for row in theorem}
            == {"COL3356_0_contact_support_set", "COL3356_1_pointwise_collar", "COL3356_2_test_variation_zero", "COL3356_3_integrated_source_warning"},
            "detail": "",
        },
        {
            "check_id": "VAL3356_4_arena_split_complete",
            "check": "arena classification separates interior bulk, material surface, exterior orbital field, and scalar monopole",
            "passed": {row["arena_id"] for row in arenas}
            == {"ARENA3356_0_interior_bulk", "ARENA3356_1_material_surface", "ARENA3356_2_exterior_orbital_field", "ARENA3356_3_scalar_monopole_contact"},
            "detail": "",
        },
        {
            "check_id": "VAL3356_5_pointwise_zero_and_surface_open",
            "check": "pointwise bulk zero passes while surface/integrated contact remains open",
            "passed": any(row["update_id"] == "ECU3356_0_pointwise_bulk" and row["value_or_bound"] == "0" for row in eps)
            and any(row["update_id"] == "ECU3356_1_surface_contact" and row["component_status"] == "OPEN" for row in eps)
            and any(row["update_id"] == "ECU3356_2_integrated_source" and row["component_status"] == "OPEN" for row in eps),
            "detail": "",
        },
        {
            "check_id": "VAL3356_6_no_local_GR_overclaim",
            "check": "full local GR/Newton claim remains false",
            "passed": any(row["gate_id"] == "GATE3356_4_local_GR_claim" and row["passed"] == "false" for row in gates),
            "detail": "",
        },
        {
            "check_id": "VAL3356_7_parent_collapse_next",
            "check": "next target attempts parent-domain signature collapse",
            "passed": any("parent-domain signature" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3356_8_write_scope_outside_formalization",
            "check": "all 3356 write targets are outside formalization-workbench",
            "passed": write_targets_outside_fw,
            "detail": f"write_targets={len(output_paths) + 1}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3356_9_overall",
            "check": "3356 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["local_sources"], local_source_rows())
    write_csv(OUTPUTS["collar_theorem"], collar_theorem_rows())
    write_csv(OUTPUTS["arena_classes"], arena_classification_rows())
    write_csv(OUTPUTS["epsilon_update"], epsilon_update_rows())
    write_csv(OUTPUTS["newton_ppn"], newton_ppn_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs())
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
