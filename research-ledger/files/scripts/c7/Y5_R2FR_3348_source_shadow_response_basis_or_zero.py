from __future__ import annotations

import csv
import hashlib
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3348-Y5-R2FR-source-shadow-response-basis-or-zero-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = [
    ("SRC3348_0_3347_doc", ROOT / "3347-Y5-R2FR-source-shadow-projector-bound-or-zero-under-AX1090.md", "3347 source-shadow zero-or-bound handoff"),
    ("SRC3348_1_3347_newtonian", OUT / "P8_Y5_R2FR_3347_LOCAL_NEWTONIAN_PROJECTION.csv", "3347 local Newtonian projection"),
    ("SRC3348_2_3347_bounds", OUT / "P8_Y5_R2FR_3347_EPSILON_SOURCE_SHADOW_BOUND_ROWS.csv", "3347 epsilon source-shadow bound rows"),
    ("SRC3348_3_3342_placeholders", OUT / "P8_Y5_R2FR_3342_MATERIAL_RESPONSE_PLACEHOLDERS.csv", "3342 material response placeholder guard"),
    ("SRC3348_4_3342_observable_map", OUT / "P8_Y5_R2FR_3342_WEP_OBSERVABLE_MAP.csv", "3342 WEP observable map"),
    ("SRC3348_5_3345_collapse", OUT / "P8_Y5_R2FR_3345_SOURCE_WEIGHT_COLLAPSE_THEOREM.csv", "3345 source-weight collapse theorem"),
    ("SRC3348_6_2616_graph", OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_STANDARD_MATTER_GRAPH_CERTIFICATE_ATTEMPT.csv", "standard matter graph certificate attempt"),
    ("SRC3348_7_2614_species", OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_DELTAW_SPECIES_BOUND_INTERFACE.csv", "species response/interface basis"),
    ("SRC3348_8_2612_prefactors", OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv", "source-prefactor classification"),
    ("SRC3348_9_3346_args", OUT / "P8_Y5_R2FR_3346_ALLOWED_ARGUMENT_INVENTORY.csv", "3346 allowed parent arguments"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3348_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3348_RESPONSE_BASIS_THEOREM.csv",
    "graph": OUT / "P8_Y5_R2FR_3348_HILBERT_GRAPH_COLLAPSE.csv",
    "basis": OUT / "P8_Y5_R2FR_3348_MATERIAL_RESPONSE_BASIS.csv",
    "bound": OUT / "P8_Y5_R2FR_3348_BOUND_REINTERPRETATION.csv",
    "promotion": OUT / "P8_Y5_R2FR_3348_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3348_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3348_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3348_VALIDATION.csv",
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


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, role in SOURCES:
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


def load_3347_bound() -> dict[str, str]:
    rows = read_csv(OUT / "P8_Y5_R2FR_3347_EPSILON_SOURCE_SHADOW_BOUND_ROWS.csv")
    for row in rows:
        if row.get("bound_id") == "BND3347_0_MICROSCOPE_TiPt_unit_response":
            return row
    raise RuntimeError("3347 MICROSCOPE Ti/Pt unit response row not found")


def response_basis_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "RTH3348_0_definition",
            "claim_piece": "R_AB is a projection, not a primitive constant",
            "mathematical_form": "eta_AB ~= epsilon_source_shadow R_AB; R_AB := P_AB[Pi_rel(T_H)] / ||T_H||",
            "derivation": "3347 split P_src into common mode plus relative projector; only the relative projector can survive measured-G calibration.",
            "status": "DERIVED_FROM_3347",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "RTH3348_1_hilbert_connected_zero",
            "claim_piece": "ordinary Hilbert-connected matter has no independent R_AB slot",
            "mathematical_form": "if T_active=T_H=sum_i T_i and sum_i nabla_mu T_i^{mu nu}=0 on a connected exchange graph, then weighted conservation forces w_i=w_* and R_AB^Hilbert=0",
            "derivation": "Noether exchange constraints on connected matter components collapse relative weights to one common measured-G calibration.",
            "status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "RTH3348_2_spurion_response_fork",
            "claim_piece": "nonzero R_AB requires an extra material/source charge basis",
            "mathematical_form": "R_AB(beta)=beta dot (chi_A-chi_B), chi in {electron fraction, proton/neutron split, EM binding, nuclear binding, lattice/boundary marker, hidden marker}",
            "derivation": "A nonzero material response is not produced by the total Hilbert stress alone; it is a source projector, spurion, or extension coefficient that must be parent-owned or empirically bounded.",
            "status": "DERIVED_FORK_TO_EXPLICIT_RESIDUAL_BASIS",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "RTH3348_3_current_verdict",
            "claim_piece": "current MTS response basis",
            "mathematical_form": "R_AB is either 0 on the signed Hilbert-connected branch, or symbolic beta dot Delta chi_AB on the unsigned extension branch",
            "derivation": "The unit response row is demoted to smoke only; future claims need either graph/parent closure or source-backed material charge rows.",
            "status": "DICHOTOMY_CLOSED_RESPONSE_NOT_CLAIMED",
            "valid_for_claim": "false",
        },
    ]


def graph_collapse_rows() -> list[dict[str, Any]]:
    return [
        {
            "graph_id": "HGC3348_0_nodes",
            "component": "ordinary atomic/nuclear matter components",
            "constraint": "nodes={charged leptons, protons, neutrons, EM binding, nuclear binding, molecular/lattice binding}",
            "derivation_use": "defines the candidate connected Hilbert-source graph whose relative weights would collapse",
            "status": "CANDIDATE_NODE_BASIS_FROM_2616_NOT_PUBLIC_SOURCED",
            "valid_for_claim": "false",
        },
        {
            "graph_id": "HGC3348_1_exchange_constraint",
            "component": "interacting component currents",
            "constraint": "nabla_mu T_i^{mu nu}=C_i^nu and sum_i C_i^nu=0; source conservation of sum_i w_i T_i requires sum_i w_i C_i^nu=0",
            "derivation_use": "nonzero exchange edges force equal source weights across connected nodes",
            "status": "DERIVED_CONDITIONAL_GRAPH_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "graph_id": "HGC3348_2_common_mode",
            "component": "connected ordinary component",
            "constraint": "w_i=w_* for all nodes in the connected component",
            "derivation_use": "w_* rescales kappa and is absorbed into measured G_N; it gives no WEP R_AB",
            "status": "DERIVED_COMMON_MODE_COLLAPSE",
            "valid_for_claim": "false",
        },
        {
            "graph_id": "HGC3348_3_decoupled_exception",
            "component": "decoupled conserved block",
            "constraint": "nabla_mu T_D^{mu nu}=0 independently",
            "derivation_use": "a decoupled block can keep an independent source weight only if it is inventoried in the local arena and bounded",
            "status": "RESIDUAL_EXCEPTION_REQUIRES_ARENA_INVENTORY",
            "valid_for_claim": "false",
        },
    ]


def material_response_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "RB3348_0_hilbert_total",
            "branch": "zero-route",
            "basis": "total Hilbert stress T_H",
            "R_TiPt": "0",
            "formula": "R_AB^Hilbert=0 after common measured-G calibration",
            "status": "EXACT_CONDITIONAL_IF_PARENT_AND_GRAPH_SIGNED",
            "claim_blocker": "parent source map and source-backed connected matter graph are not yet fully signed",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "RB3348_1_common_mode",
            "branch": "calibration-route",
            "basis": "universal source scale C_0",
            "R_TiPt": "0",
            "formula": "G_N=G_*(1+C_0), so differential WEP response cancels",
            "status": "DERIVED_COMMON_MODE_NOT_LOCAL_WEP_RESIDUAL",
            "claim_blocker": "global/cosmological calibration treated separately",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "RB3348_2_spurion_vector",
            "branch": "finite-bound-route",
            "basis": "chi_k material/source charges",
            "R_TiPt": "beta dot (chi_Ti-chi_Pt)",
            "formula": "eta_TiPt ~= epsilon_source_shadow beta_k Delta chi_k(Ti,Pt)",
            "status": "SYMBOLIC_EXTENSION_BASIS_NOT_PARENT_DERIVED",
            "claim_blocker": "need source-backed Ti/Pt material composition, binding-energy convention, and beta normalization",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "RB3348_3_unit_smoke",
            "branch": "smoke-only-route",
            "basis": "private unit response",
            "R_TiPt": "1",
            "formula": "epsilon_source_shadow <= eta_TiPt for schema testing only",
            "status": "DEMOTED_SCHEMA_SMOKE_ONLY",
            "claim_blocker": "unit response is not a derived MTS material basis",
            "valid_for_claim": "false",
        },
    ]


def bound_reinterpretation_rows() -> list[dict[str, Any]]:
    previous = load_3347_bound()
    epsilon_bound = float(previous["epsilon_bound"])
    return [
        {
            "bound_id": "BR3348_0_hilbert_zero_branch",
            "branch": "zero-route",
            "observable": "eta_TiPt",
            "response_factor": "R_TiPt=0",
            "bound_or_theorem": "no finite division is used; source-shadow response is absent if Hilbert-connected parent branch closes",
            "numeric_value": "theorem_zero_conditional",
            "source_path": str(OUT / "P8_Y5_R2FR_3347_LOCAL_NEWTONIAN_PROJECTION.csv"),
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BR3348_1_symbolic_spurion_branch",
            "branch": "finite-bound-route",
            "observable": "eta_TiPt",
            "response_factor": "R_TiPt=beta dot Delta chi_TiPt",
            "bound_or_theorem": "|epsilon_source_shadow| <= 4.245906e-15 / |beta dot Delta chi_TiPt|",
            "numeric_value": "symbolic_until_chi_and_beta_sourced",
            "source_path": previous["source_path"],
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BR3348_2_unit_smoke_branch",
            "branch": "smoke-only-route",
            "observable": "eta_TiPt",
            "response_factor": "R_TiPt=1",
            "bound_or_theorem": "|epsilon_source_shadow| <= 4.245906e-15",
            "numeric_value": f"{epsilon_bound:.6e}",
            "source_path": previous["source_path"],
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3348_0_response_dichotomy",
            "claim": "R_AB is either zero on the Hilbert-connected branch or an explicit spurion/charge response",
            "passed": "true",
            "reason": "3348 derives the Hilbert-collapse/spurion-fork structure",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3348_1_hilbert_zero_parent_signed",
            "claim": "R_AB=0 is parent-signed for current MTS ordinary matter",
            "passed": "false",
            "reason": "parent source-map and source-backed connected graph certificate remain unsigned",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3348_2_unit_response_demoted",
            "claim": "the previous unit response is treated only as smoke",
            "passed": "true",
            "reason": "3348 preserves it only in BR3348_2_unit_smoke_branch with valid_for_claim=false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3348_3_finite_response_claim",
            "claim": "finite epsilon_source_shadow bound is claim-ready in MTS basis",
            "passed": "false",
            "reason": "beta and Delta chi_TiPt are symbolic until source-backed material composition and normalization are supplied",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3348_4_local_GR_claim",
            "claim": "local GR/Newton source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "source response basis is narrowed but not parent-signed or fully sourced",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3348_0",
            "question": "Did 3348 derive R_AB as an MTS-owned material number?",
            "answer": "not as a numeric claim",
            "reason": "the derivation shows R_AB vanishes on the Hilbert-connected branch; nonzero R_AB is a symbolic spurion/charge basis requiring source-backed material rows",
            "next_action": "try to close the source-backed ordinary matter graph certificate before building empirical charge tables",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3348_1",
            "question": "Did 3348 move beyond missing-ledger work?",
            "answer": "yes",
            "reason": "it demotes the unit response, proves the response fork, and identifies the lower-scrutiny route: no independent ordinary R_AB slot",
            "next_action": "3349 should source-sign the connected Hilbert matter graph or explicitly fail into a material-composition table",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3349-Y5-R2FR-source-backed-ordinary-matter-graph-certificate-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3349_source_backed_ordinary_matter_graph_certificate.py",
            "objective": "source-sign the connected ordinary matter Hilbert graph enough to promote the R_AB=0 no-independent-slot route, or explicitly fail to the material charge-table branch",
            "why_next": "this is lower-scrutiny than fitting arbitrary WEP charges: if the graph closes, source-shadow material response is common-mode only",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3349b-Y5-R2FR-TiPt-material-charge-table-nonclaim.md",
            "target_script": "scripts/Y5_R2FR_3349b_TiPt_material_charge_table_nonclaim.py",
            "objective": "if the graph route fails, acquire source-backed Ti/Pt composition and build symbolic/numeric Delta chi rows without claiming MTS local GR",
            "why_next": "needed only for the finite-bound spurion branch R_TiPt=beta dot Delta chi_TiPt",
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
            "# 3348 — Source-Shadow Response Basis Or Zero Under AX1090",
            f"Generated: `{RUN_UTC}`",
            "## Summary\n"
            "- This checkpoint attacks the `R_AB` material/source response factor exposed by 3347.\n"
            "- The important result is a fork: on the ordinary connected Hilbert-source branch, `R_AB=0` after measured-`G_N` calibration; a nonzero `R_AB` is not Hilbert stress, it is an explicit spurion/projector charge basis.\n"
            "- The previous `R_TiPt=1` row is demoted to schema smoke only, not physics.\n"
            "- The lower-scrutiny next route is to source-sign the ordinary matter exchange graph; if that fails, build a source-backed Ti/Pt charge table for the finite-bound branch.",
            "## Response Basis Theorem\n" + markdown_table(response_basis_theorem_rows()),
            "## Hilbert Graph Collapse\n" + markdown_table(graph_collapse_rows()),
            "## Material Response Basis\n" + markdown_table(material_response_basis_rows()),
            "## Bound Reinterpretation\n" + markdown_table(bound_reinterpretation_rows()),
            "## Promotion Gates\n" + markdown_table(promotion_gate_rows()),
            "## Decision Ledger\n" + markdown_table(decision_rows()),
            "## Next Target\n" + markdown_table(next_target_rows()),
        ]
    ) + "\n"


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = source_rows()
    theorem = response_basis_theorem_rows()
    basis = material_response_basis_rows()
    bound = bound_reinterpretation_rows()
    gates = promotion_gate_rows()
    formalization_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3348_0_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3348_1_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3348_2_outputs_parse",
            "check": "all 3348 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3348_3_theorem_fork_present",
            "check": "theorem includes definition, Hilbert zero, spurion fork, and verdict",
            "passed": {row["theorem_id"] for row in theorem}
            == {"RTH3348_0_definition", "RTH3348_1_hilbert_connected_zero", "RTH3348_2_spurion_response_fork", "RTH3348_3_current_verdict"},
            "detail": "",
        },
        {
            "check_id": "VAL3348_4_basis_routes_present",
            "check": "basis rows include Hilbert zero, common mode, symbolic spurion, and unit smoke",
            "passed": {row["basis_id"] for row in basis}
            == {"RB3348_0_hilbert_total", "RB3348_1_common_mode", "RB3348_2_spurion_vector", "RB3348_3_unit_smoke"},
            "detail": "",
        },
        {
            "check_id": "VAL3348_5_unit_smoke_demoted",
            "check": "unit response remains nonclaim and explicitly demoted",
            "passed": any(row["basis_id"] == "RB3348_3_unit_smoke" and row["valid_for_claim"] == "false" and "DEMOTED" in row["status"] for row in basis),
            "detail": "",
        },
        {
            "check_id": "VAL3348_6_symbolic_branch_no_fake_numeric",
            "check": "symbolic spurion branch has no fabricated numeric response",
            "passed": any(row["bound_id"] == "BR3348_1_symbolic_spurion_branch" and row["numeric_value"] == "symbolic_until_chi_and_beta_sourced" for row in bound),
            "detail": "",
        },
        {
            "check_id": "VAL3348_7_no_overclaim",
            "check": "R_AB zero, finite response, and local-GR claim gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3348_1_hilbert_zero_parent_signed", "GATE3348_3_finite_response_claim", "GATE3348_4_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3348_8_next_target_graph_first",
            "check": "next target prioritizes ordinary matter graph certificate",
            "passed": any("ordinary matter Hilbert graph" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3348_9_bound_numeric_finite_for_smoke_only",
            "check": "unit-smoke inherited numeric bound remains positive finite",
            "passed": any(
                row["bound_id"] == "BR3348_2_unit_smoke_branch"
                and math.isfinite(float(row["numeric_value"]))
                and float(row["numeric_value"]) > 0.0
                and row["valid_for_claim"] == "false"
                for row in bound
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3348_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3348_11_overall",
            "check": "3348 validation overall",
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
    write_csv(OUTPUTS["sources"], source_rows())
    write_csv(OUTPUTS["theorem"], response_basis_theorem_rows())
    write_csv(OUTPUTS["graph"], graph_collapse_rows())
    write_csv(OUTPUTS["basis"], material_response_basis_rows())
    write_csv(OUTPUTS["bound"], bound_reinterpretation_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
